'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

import os

from tabulate import tabulate
from typing import List, Optional

from business_object.joueur import Joueur
from business_object.maitre_jeu import MaitreJeu
from business_object.personnage import Personnage
from dao.joueur_dao import JoueurDao
from dao.maitre_jeu_dao import MaitreJeuDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from view.session import Session
from dao.message_dao import MessageDao


class JoueurService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer(self, pseudo, nom, prenom, mail) -> Optional[Joueur]:
        '''Service de création d'un joueur

        Parameters
        ----------
        pseudo : str
            pseudo du joueur
        nom : str
            nom du joueur
        prenom : str
            prenom du joueur
        mail : str
            mail du joueur

        Returns
        -------
        Joueur : le joueur créé
        '''
        print("Service : Création du Joueur")

        nouveau_joueur = Joueur(pseudo, nom, prenom, mail)
        JoueurDao().creer(nouveau_joueur)

        print("Service : Création du Joueur - Terminé")

        return nouveau_joueur

    def rejoindre_table(self, table, joueur, personnage) -> bool:
        '''Rejoindre une table s'il y a de la place

        Parameters
        ----------
        table : Table
            la table sur laquelle on ajoute le joueur
        joueur : Joueur
            Joueur à ajouter
        personnage : Personnage
            Personnage choisi par le joueur
        '''

        print("Service : Rejoindre une table")

        success = False

        # TODO verifier que le joueur est libre a cet horaire

        # y a t il encore de la place a la table
        nb_joueurs_table = TableJeuDao().get_nb_joueurs(table)

        if nb_joueurs_table <= table.nb_joueurs_max:
            success = joueur_dao.ajouter_joueur(table, joueur, personnage)
        else:
            print("Impossible d'ajouter de nouveaux joueurs à la table")
            print("Nombre de joueurs maximum : " + table.nb_joueurs_max)
            print("Nombre de joueurs actuellement : " + nombre_actuel_joueurs)

        print("Service : Rejoindre une table - Terminé")

        return success

    def lister_tous(self):
        '''Service pour lister tous les joueurs

        Returns
        -------
        liste[Joueur]
        '''
        print("Service : Lister tous les joueurs")
        return JoueurDao().lister_tous()

    def trouver_par_pseudo(self, pseudo):
        '''Trouver un joueur à partir de son pseudo

        Returns
        -------
        Joueur
        '''
        print("Service : Trouver par pseudo ({})".format(pseudo))
        joueur = JoueurDao().trouver_par_pseudo(pseudo)
        if joueur:
            joueur.liste_personnages = PersonnageDao().lister_par_joueur(joueur)
        return joueur

    def creation_personnage_autorisee(self) -> bool:
        '''Dit si le joueur n'a pas atteint le nombre maximum de Personnages
        '''
        joueur = Session().user
        return len(joueur.liste_personnages) < int(os.environ["NB_MAX_PERSONNAGES_PAR_JOUEUR"])

    def creer_personnage(self, nom, classe2, race, niveau):
        '''
        '''
        print("Service : Création de personnage")

        # TODO verifier que le nom du personnage n'existe pas déjà

        # TODO appel API pour obtenir competences

        perso = Personnage(id_personnage=None,
                           nom=nom,
                           classe=classe2,
                           race=race,
                           niveau=niveau)

        created = PersonnageDao().creer(perso)

        print("Service : Création de personnage - Terminé")

        return perso

    def lister_personnages(self):
        '''Lister les personnages d'une utilisateur

        Returns
        -------
        '''

        print("Service : Liste des personnages")

        joueur = Session().user

        personnages = PersonnageDao().lister_par_joueur(joueur)

        entetes = ["id", "Nom", "Classe",
                   "Race", "Niveau"]
        personnages_as_list = [p.as_list() for p in personnages]

        resultat = "Liste des personnages \n" + tabulate(tabular_data=personnages_as_list,
                                                         headers=entetes,
                                                         tablefmt="psql",
                                                         floatfmt=".2f") + "\n"

        print("Service : Liste des personnages - Terminé")

        return resultat

    def supprimer_personnage(self, perso_a_supprimer):
        '''Supprimer un personnage d'un utilisateur

        Returns
        -------
        '''

        print("Service : Suppression d'un personnage")

        joueur = Session().user

        # vérifier si le personnage n'est pas assis à une table
        perso_non_utilise = (
            PersonnageDao().lister_tables(perso_a_supprimer) == 0)

        if perso_non_utilise:
            statut_suppression = PersonnageDao().supprimer(perso_a_supprimer)
            # Supprimer le personnage de la liste du joueur
            print(f"suppression de {perso_a_supprimer.nom}")
            for el in joueur.liste_personnages:
                print(el.nom)
            joueur.liste_personnages.remove(perso_a_supprimer)
        else:
            statut_suppression = [
                False, f"Le personnage {perso_a_supprimer.nom} est déjà utilisé sur une table"]

        print("Service : Suppression de personnage - Terminé")

        return statut_suppression

    def supprimer(self, compte):
        '''Supprimer le compte d'un joueur

        compte: Joueur
        Returns
        -------
        '''

        print("Service : Suppression de compte")

        joueur = Session().user

        pb_rencontre = 0
        pb_list_joueur = []
        # Enlever les personnages des tables où ils sont utilisés
        # Dans la DAO, le lien entre le joueur et sa table se fait via les personnages
        # Supprimer un personnage d'un table revient à supprimer le joueur
        for el in compte.liste_personnages:
            perso_utilise = (
                PersonnageDao().lister_tables(el) > 0)
            if perso_utilise:
                perso_enleve_table = PersonnageDao().quitter_table(el)
                if not perso_enleve_table:
                    pb_rencontre += 1
                    pb_list_joueur.append(el.nom)
        if pb_rencontre != 0:
            print("problème rencontré au moment d'enlever ce(s) personnage(s)" +
                  "d'une table:\n" +
                  f"{pb_list_joueur}")

        # Supprimer les personnages
        # Attention: lors de la suppression du premier personnage de la liste
        # dans la DAO, il est aussi supprimé de la liste de persos du joueur
        # Le deuxième perso est alors en premier sur la liste
        # --> Parcourir la liste dans le sens normal entraine une erreur
        #  --> besoin de parcourir la liste à l'envers
        perso_list = []
        for el in reversed(compte.liste_personnages):
            statut_suppr_perso = self.supprimer_personnage(el)

        # Enlever le joueur des tables où il est assis en tant que maitre du jeu
        if type(compte) == MaitreJeu:
            statut_suppr_mj = MaitreJeuDao().quitter_table(compte)

        # Supprimer le compte du joueur
        statut_suppression = JoueurDao().supprimer_compte(compte)

        print("Service : Suppression de compte - Terminé")

        return statut_suppression

    def voir_messages(self):
        '''Afficher les messages envoyés à un utilisateur

        Returns
        -------
        '''

        print("Service : voir les messages")

        joueur = Session().user
        #print('00')

        messages = MessageDao().lister_par_joueur(joueur)
        #print('aa')

        entetes = ["id_message", "id_joueur", "Contenu", "Lu", "Date_création"]
        message_as_list = [msg.as_list() for msg in messages]

        #print('bb')

        resultat = "Votre Messages \n" + tabulate(tabular_data=message_as_list,
                                                  headers=entetes,
                                                  tablefmt="psql",
                                                  floatfmt=".2f") + "\n"

        print("Service : voir les messages - Terminé")

        return resultat
