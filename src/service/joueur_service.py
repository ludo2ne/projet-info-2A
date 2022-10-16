'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

import os
from tabulate import tabulate

from business_object.joueur import Joueur
from business_object.personnage import Personnage
from dao.joueur_dao import JoueurDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from view.session import Session


class JoueurService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer(self, pseudo, nom, prenom, mail):
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

        # TODO vérifier si le personnage n'est pas assis à une table

        statut_suppression = PersonnageDao().supprimer(perso_a_supprimer)
        # Supprimer le personnage de la liste du joueur
        joueur.liste_personnages.remove(perso_a_supprimer)

        print("Service : Suppression de personnage - Terminé")

        return statut_suppression
