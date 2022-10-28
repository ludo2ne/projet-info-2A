'''
Module maitre_jeu_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

import os

from tabulate import tabulate
from typing import List, Optional

from view.session import Session

from service.joueur_service import JoueurService

from dao.joueur_dao import JoueurDao
from dao.maitre_jeu_dao import MaitreJeuDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from dao.message_dao import MessageDao
from dao.table_jeu_dao import TableJeuDao
from dao.seance_dao import SeanceDao

from business_object.joueur import Joueur
from business_object.maitre_jeu import MaitreJeu
from business_object.personnage import Personnage
from business_object.table_jeu import TableJeu


class MaitreJeuService:
    '''Classe contenant les méthodes de service de MaitreJeu

    Attributes
    ----------
    None

    Methods
    -------
    lister_tables(mj : Joueur) : list
    quitter_table(mj : Joueur, seance : int): list
    gerer_table(id_seance : int , scenario : str, infos_complementaires : str): str
    voir_tables_gerees() : str
    '''

    def lister_tables(self, mj) -> list:
        '''Service de listing de tables du mj

        Parameters
        ----------
        mj : Joueur
            il s'agit du maitre du jeu

        Returns
        -------
        table_list : list
        '''
        print("Service : Listing de TableJeu du mj")

        table_list = MaitreJeuDao().lister_tables_mj(mj)

        print("Service : Listing de TableJeu du mj - Terminé")
        return table_list

    def quitter_table(self, mj, seance) -> list:
        '''Service de résiliation de tables du mj

        Parameters
        ----------
        mj : Joueur
            le maître du jeu
        seance : int
            numéro de la séance

        Returns
        -------
        list
        '''
        print("Service : Résiliation de TableJeu du mj")

        # Creation d'un dictionnaire id_seance --> description_seance
        liste_seance = SeanceDao().lister_toutes()
        dict_seance = {}
        for el in liste_seance:
            dict_seance[f"{el.id_seance}"] = el.description

        # instanciation de la table à supprimer
        table_correspondante = TableJeuDao().lister(mj=mj, seance=seance)[0]
        # Liste des joueurs assis à cette table
        joueur_list = TableJeuDao().joueurs_assis(table_correspondante)

        statut_quitter_table = MaitreJeuDao().quitter_table(mj, seance)
        err_message = ""
        if not statut_quitter_table:
            err_message = f"Vous n'avez pas pu quitter la table.\n"
        else:
            # notification de l'administrateur
            message = f"Le Maitre du Jeu {mj.pseudo} a quitté la table {table_correspondante.id_table} du {dict_seance[str(table_correspondante.id_seance)]}."
            admin = JoueurService().trouver_par_pseudo("admin")
            statut_notif_admin = MessageDao().creer(admin, message)
            if not statut_notif_admin:
                err_message = "L'administrateur n'a pas pu être notifié.\n"
            admin = None

            # notification des joueurs assis
            for player in joueur_list:
                message = f"Le Maitre du Jeu {mj.pseudo} a quitté la table {table_correspondante.id_table} du {dict_seance[str(table_correspondante.id_seance)]}."
                statut_notif_joueur = MessageDao().creer(player, message)
                print(f"Message au joueur {player.pseudo}")
                if not statut_notif_joueur:
                    err_message += f"Le joueur {player.pseudo} n'a pas pu être notifié.\n"

        print("Service : Résiliation de TableJeu du mj - Terminé")
        return [statut_quitter_table, err_message]

    def gerer_table(self, seance, scenario, infos_complementaires) -> str:
        '''Service de gerer une table pour mj

        Parameters
        ----------
        seance : Seance
            Séance concernée
        scenario : str
            nom du scénario
        infos_complementaires : str
            informations complémentaires

        Returns
        -------
        resultat : str
        '''
        print("Service : Gestion d'une table jeu du mj")
        mj = Session().user

        # Vérification de la disponibilité d'un mj pour voir si le mj peut gérer une table
        # voir si le mj a deja inscrit pour une meme seance en tant que mj
        table_list_mj = []
        table_list_mj = MaitreJeuDao().lister_tables_mj(mj)
        for i in range(len(table_list_mj)):
            if table_list_mj[i][1] == seance.id_seance:
                resultat = "mj non libre"
                return resultat
        # voir si le mj a deja inscrit pour une meme seance en tant que joueur
        table_list_j = TableJeuDao().lister(joueur=mj, seance=None)
        for table_jeu in table_list_j:
            if table_jeu.id_seance == seance.id_seance:
                resultat = "mj non libre"
                return resultat

        # Trouver une table libre
        table_jeu = TableJeuDao().trouver_table_libre(seance)
        if not table_jeu:
            resultat = "non table libre"
            return resultat

        table_jeu.scenario = scenario
        table_jeu.infos_complementaires = infos_complementaires

        # Mettre en place la gestion de table
        if TableJeuDao().gerer_par_mj(table_jeu, mj):
            resultat = "OK"

        print("Service : Gestion d'une table jeu du mj - Terminé")
        return resultat

    def voir_tables_gerees(self) -> str:
        '''Affiche les tables ou le mj est

        Parameters
        ----------
        None

        Returns
        -------
        resultat : str
        '''
        print("Service : Voir programme")

        joueur = Session().user

        table_jeu = TableJeuDao().lister(mj=joueur)

        entetes = ["séance", "id_table", "scénario", "Personnages"]

        entetes_perso = ["nom", "classe", "race",
                         "niveau", "competence", "langue_parlée"]

        # liste de liste des persos de chaque table
        list_perso_des_tables = [t.liste_perso() for t in table_jeu]

        table_as_list = [t.as_list()[0:len(entetes)-1] for t in table_jeu]
        print(table_as_list)

        i = 0
        for table in table_jeu:
            perso_as_list = [p.as_list()[1:len(entetes_perso)+1]
                             for p in table.personnages]
            resultat_perso = tabulate(tabular_data=perso_as_list,
                                      headers=entetes_perso,
                                      tablefmt="psql",
                                      floatfmt=".2f") + "\n"

            table_as_list[i].append(resultat_perso)
            i += 1

        resultat = "Liste des tables \n" + tabulate(tabular_data=table_as_list,
                                                    headers=entetes,
                                                    tablefmt="psql",
                                                    floatfmt=".2f") + "\n"

        print("Service : Voir programme - Terminé")

        return resultat

    def devenir_mj(self):
        '''Service de passage au statut mj
        '''
        print("Service : Passage au statut mj")

        joueur = Session().user
        statut = MaitreJeuDao().devenir_mj()
        if statut:
            Session().user = MaitreJeu(joueur)

        print("Service : Passage au statut mj - Terminé")
        return statut
