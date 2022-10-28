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

from view.session import Session

from business_object.joueur import Joueur
from business_object.maitre_jeu import MaitreJeu
from business_object.personnage import Personnage

from dao.joueur_dao import JoueurDao
from dao.maitre_jeu_dao import MaitreJeuDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from dao.message_dao import MessageDao
from dao.message_dao import MessageDao
from dao.seance_dao import SeanceDao


class JoueurService:
    '''
    Classe contenant les méthodes de service de Joueur

    Attributes
    ----------
        None

    Methods
    -------
        creer(pseudo : str, nom : str, prenom : str) : Joueur
            création d'un joueur
        rejoindre_table(table : TableJeu, joueur : Joueur, personnage : Personnage) : bool
            permet au joueur connecté de rejoindre une table
        lister_tous() : list[Joueur]
            lister tous les joueurs
        trouver_par_pseudo(pseudo : str) : Joueur
            trouver un joueur par son pseudo
        creation_personnage_autorisee() : bool
            permet de savoir si le joueur connecté a la possibilité de créer un personnage 
        creer_personnage(nom : str, classe2 : str, race : str, niveau : int) : Personnage
            permet au joueur connecté de créer un personnage
        lister_personnages() : str
            permet au joueur connecter de lister ses personnages
        supprimer_personnage(perso_a_supprimer : Personnage, joueur : Joueur) : list[bool,str]
            permet au joueur connecté de supprimer un personnage qu'il possède
        supprimer(compte : Joueur) : list[bool,str]
            permet de supprimer son compte joueur
        voir_son_programme() : str 
            permet au joueur connecté de voir les informations des tables sur lesquelles il possède un personnage
        voir_messages() : str
            permet au joueur connecté de voir ses messages
        quitter_table(id_table : str) : bool
            permet au joueur connecté de quitter une table
        inscrire_table(table_choisie : TableJeu, perso_choisi : Personnage) : bool
            permet au joueur connecté de s'inscrire à une table
    '''

    def creer(self, pseudo, nom, prenom, mail) -> Joueur:
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
        nouveau_joueur : Joueur
            Le joueur crée
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

        Returns
        -------
        succes : bool
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

    def lister_tous(self) -> list[Joueur]:
        '''Service pour lister tous les joueurs

        Parameters
        ----------
        None

        Returns
        -------
        liste[Joueur]
        '''

        print("Service : Lister tous les joueurs")
        return JoueurDao().lister_tous()

    def trouver_par_pseudo(self, pseudo) -> Joueur:
        '''Trouver un joueur à partir de son pseudo

        Parameters
        ----------
        pseudo : str
            pseudo du joueur à trouver

        Returns
        -------
        joueur : Joueur
            joueur trouvé par le pseudo
        '''

        print("Service : Trouver par pseudo ({})".format(pseudo))
        joueur = JoueurDao().trouver_par_pseudo(pseudo)
        if joueur:
            joueur.liste_personnages = PersonnageDao().lister_par_joueur(joueur)
        return joueur

    def creation_personnage_autorisee(self) -> bool:
        '''Dit si le joueur n'a pas atteint le nombre maximum de Personnages

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True si le joueur peut encore créer des personnages (si le joueur possède pas trop de personnage)
        '''
        joueur = Session().user
        return len(joueur.liste_personnages) < int(os.environ["NB_MAX_PERSONNAGES_PAR_JOUEUR"])

    def creer_personnage(self, nom, classe2, race, niveau, competence, langues_parlees) -> Personnage:
        '''Permet la création d'un personnage

        Parameters
        ----------
        nom : str
            nom du personnage
        classe2 : str
            classe du personnage
        race : str
            race du personnage
        niveau : int
            niveau du personnage
        competence : str
            competence du personnage
        langue : str
            langue du personnage

        Returns
        -------
        perso : Personnage
            retourne le personnage crée
        '''
        print("Service : Création de personnage")

        # TODO verifier que le nom du personnage n'existe pas déjà

        perso = Personnage(id_personnage=None,
                           nom=nom,
                           classe=classe2,
                           race=race,
                           niveau=niveau,
                           competence=competence,
                           langues_parlees=langues_parlees
                           )

        created = PersonnageDao().creer(perso)

        print("Service : Création de personnage - Terminé")

        return perso

    def lister_personnages(self) -> str:
        '''Lister les personnages d'une utilisateur

        Parameters
        ----------
        None

        Returns
        -------
        resultat : str
            renvoie la liste des personnage sous forme tabulée (c'est un str)
        '''

        print("Service : Liste des personnages")

        joueur = Session().user

        personnages = PersonnageDao().lister_par_joueur(joueur)

        entetes = ["id", "Nom", "Classe",
                   "Race", "Niveau", "Compétence", "Langues parlées"]
        personnages_as_list = [p.as_list() for p in personnages]

        resultat = "Liste des personnages \n" + tabulate(tabular_data=personnages_as_list,
                                                         headers=entetes,
                                                         tablefmt="psql",
                                                         floatfmt=".2f") + "\n"

        print("Service : Liste des personnages - Terminé")

        return resultat

    def supprimer_personnage(self, perso_a_supprimer, joueur=None) -> list[bool, str]:
        '''Supprimer un personnage d'un utilisateur

        Parameters
        ----------
        perso_a_supprimer : Personnage
            personnage à supprimer
        joueur : Joueur
            joueur qui possède le personnage à supprimer

        Returns
        -------
        statut_suppression : list[bool,str]
        '''
        print("Service : Suppression d'un personnage")

        if not joueur:
            joueur = Session().user

        # vérifier si le personnage n'est pas assis à une table
        perso_non_utilise = (
            PersonnageDao().lister_tables(perso_a_supprimer) == 0)

        if perso_non_utilise:
            statut_suppression = [
                PersonnageDao().supprimer(perso_a_supprimer), ""]
            # Supprimer le personnage de la liste du joueur
            print(f"suppression de {perso_a_supprimer.nom}")
            for el in joueur.liste_personnages:
                print(el.nom)
            joueur.liste_personnages.remove(perso_a_supprimer)
        else:
            statut_suppression = [
                False, f"Le personnage {perso_a_supprimer.nom} est déjà utilisé sur une table.\n"]

        print("Service : Suppression de personnage - Terminé")

        return statut_suppression

    def supprimer(self, compte):
        '''Supprimer le compte d'un joueur

        Params
        ------
        * compte : Joueur
            * Compte du joueur à supprimer

        Returns
        -------
        * True si le compte a bien été supprimé
        * False sinon
        '''

        print("Service : Suppression de compte")

        joueur = Session().user

        pb_rencontre = 0
        pb_list_joueur = []
        err_message = ""
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
                    err_message += f"Problème rencontré au moment d'enlever le personnage {el.nom} d'une table.\n"
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
            statut_suppr_perso = self.supprimer_personnage(el, compte)
            err_message += statut_suppr_perso[1]

        # Enlever le joueur des tables où il est assis en tant que maitre du jeu
        liste_seance = SeanceDao().lister_toutes()
        dict_seance = {}
        for el in liste_seance:
            dict_seance[f"{el.id_seance}"] = el.description

        if type(compte) == MaitreJeu:
            table_list = MaitreJeuDao().lister_tables_mj(compte)
            admin = self.trouver_par_pseudo("admin")
            for el in table_list:
                table_correspondante = TableJeuDao().trouver_par_id(el[1])
                joueur_list = TableJeuDao().joueurs_assis(table_correspondante)
                statut_suppr_mj = MaitreJeuDao().quitter_table(compte, el[1])
                if not statut_suppr_mj:
                    err_message += f"Le Maitre du Jeu {compte.pseudo} n'a pas pu quitter la table {el[0]}\n"
                else:
                    # notifier l'administrateur
                    message = f"Le Maitre du Jeu {compte.pseudo} a quitté la table {el[0]} de la séance du {dict_seance[str(el[1])]}"
                    statut_notif_admin = MessageDao().creer(admin, message)
                    if not statut_notif_admin:
                        err_message += "L'administrateur n'a pas pu être notifié.\n"

                    # notifier les joueurs assis à la table
                    for player in joueur_list:
                        message = f"Le Maitre du Jeu {compte.pseudo} a quitté la table {el[0]} de la séance du {dict_seance[str(el[1])]}"
                        statut_notif_joueur = MessageDao().creer(player, message)
                        if not statut_notif_joueur:
                            err_message += f"Le joueur {player.pseudo} n'a pas pu être notifié.\n"

            admin = None

        # Supprimer le compte du joueur
        statut_suppression = JoueurDao().supprimer_compte(compte)
        if not statut_suppression:
            err_message += f"Le compte du joueur {compte.pseudo} n'a pas pu être supprimé.\n"

        print("Service : Suppression de compte - Terminé")

        return [statut_suppression, err_message]

    def voir_son_programme(self) -> str:
        '''Affiche les tables ou le joueur est

        Parameters
        ----------
        None

        Returns
        -------
        resultat : str
            renvoie le résumé des tables du joueur
        '''
        print("Service : Voir programme")

        joueur = Session().user

        table_jeu = TableJeuDao().lister(joueur=joueur)

        if type(joueur) == MaitreJeu:
            table_jeu_mj = TableJeuDao().lister(mj=joueur)
            table_jeu += table_jeu_mj

        entetes = ["Séance", "Numéro Table", "Scénario",
                   "Maître du jeu", "Personnage joué"]

        # liste de liste des persos de chaque table
        list_perso_des_tables = [t.liste_perso() for t in table_jeu]

        # Gros mic-mac pour replacer les tables dans l'ordre chronologique...
        liste_provisoire = []
        for t in table_jeu:
            listbid = t.as_list()
            listbid.append(t)
            liste_provisoire.append(listbid)
        liste_provisoire.sort()
        table_jeu = [t[-1] for t in liste_provisoire]
        table_as_list = [t[0:len(t)-1] for t in liste_provisoire]

        for t_list in table_as_list:
            seance = SeanceDao().trouver_par_id(t_list[0])
            t_list[0] = seance.description

        i = 0
        for table in table_jeu:
            # On regarde si le joueur joue à la table
            for perso in table.personnages:
                for perso_joueur in joueur.liste_personnages:
                    if perso_joueur.id_personnage == perso.id_personnage:
                        table_as_list[i].append(perso_joueur.nom)
                        print(table.id_table, i, "joueur")
                        i += 1
            # ou s'il y officie en tant que MJ
            if table.maitre_jeu.id_joueur == joueur.id_joueur:
                print(table.id_table, i, "mj")
                i += 1

        resultat = "Liste des tables \n" + tabulate(tabular_data=table_as_list,
                                                    headers=entetes,
                                                    tablefmt="psql",
                                                    floatfmt=".2f") + "\n"

        print("Service : Voir programme - Terminé")

        return resultat

    def voir_messages(self) -> str:
        '''Afficher les messages envoyés à un utilisateur

        Parameters
        ----------
        None

        Returns
        -------
        resultat : str
            renvoie le résumé des messages du joueur
        '''

        print("Service : voir les messages")

        joueur = Session().user
        # print('00')

        messages = MessageDao().lister_par_joueur(joueur)
        # print('aa')

        entetes = ["id_message", "id_joueur", "Contenu", "Lu", "Date_création"]
        message_as_list = [msg.as_list() for msg in messages]

        # print('bb')

        resultat = "Votre Messages \n" + tabulate(tabular_data=message_as_list,
                                                  headers=entetes,
                                                  tablefmt="psql",
                                                  floatfmt=".2f") + "\n"

        print("Service : voir les messages - Terminé")

        return resultat

    def quitter_table(self, id_table) -> bool:
        '''Permet au joueur de quitter sa table

        Parameters
        ----------
        id_table : int
            numéro id de la table dont le joueur souhaite quitter

        Returns
        -------
            statut_suppression : bool
        '''
        print("Service : Quitter une table")

        joueur = Session().user
        table = TableJeuDao().trouver_par_id(id_table)

        for perso_table in table.personnages:
            for perso_joueur in joueur.liste_personnages:
                if perso_joueur.id_personnage == perso_table.id_personnage:
                    personnage = PersonnageDao().trouver_par_id(perso_table.id_personnage)

        statut_suppression = PersonnageDao().quitter_table(personnage, table)

        print("Service : Suppression de personnage - Terminé")

        return statut_suppression

    def inscrire_table(self, table_choisie, perso_choisi) -> bool:
        '''Inscrire un personnage à une table

        Parameters
        ----------
        table_choisie : int
            choisir la table sur laquelle s'inscrire
        perso_choisi : Personnage
            Personnage que le joueur souhaite inscrire à la table

        Returns
        -------
        statut : bool
        '''

        print("Service : Inscrire un personnage sur une table")
        statut = PersonnageDao().inscrire_table(
            table=table_choisie, personnage=perso_choisi)
        print("Service : Inscrire un personnage sur une table - Terminé")

        return statut
