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
from business_object.table_jeu import TableJeu
from dao.joueur_dao import JoueurDao
from dao.maitre_jeu_dao import MaitreJeuDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from dao.message_dao import MessageDao
from service.joueur_service import JoueurService
from view.session import Session
from dao.table_jeu_dao import TableJeuDao


class MaitreJeuService:
    '''Classe contenant les méthodes de service de MaitreJeu

    Attributes
    ----------
    None

    Methods
    -------
    lister_tables(mj : Joueur) : list
    quitter_table(mj : Joueur, seance : int): list
    gerer_table(id_seance : int , scenario : str, info_comple : str): str
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

        statut_quitter_table = MaitreJeuDao().quitter_table(mj, seance)
        err_message = ""
        if not statut_quitter_table:
            err_message = f"Vous n'avez pas pu quitter la table.\n"
        else:
            message = f"Le Maitre du Jeu {mj.pseudo} a quitté la table."
            admin = JoueurService().trouver_par_pseudo("admin")
            statut_notif_admin = MessageDao().creer(admin, message)
            if not statut_notif_admin:
                err_message = "L'administrateur n'a pas pu être notifié.\n"
            admin = None

        print("Service : Résiliation de TableJeu du mj - Terminé")
        return [statut_quitter_table, err_message]

    def gerer_table(self, id_seance, scenario, info_comple) -> str:
        '''Service de gerer une table pour mj

        Parameters
        ----------
        id_seance : int
            numéro de la séance
        scenario : str
            nom du scénario
        info_comple : str
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
            if table_list_mj[i][1] == id_seance:
                resultat = "mj non libre"
                return resultat
        # voir si le mj a deja inscrit pour une meme seance en tant que joueur
        table_list_j = TableJeuDao().lister(joueur=mj, seance=None)
        for table_jeu in table_list_j:
            if table_jeu.id_seance == id_seance:
                resultat = "mj non libre"
                return resultat

        # Vérification de la disponibilité de table jeu
        table_list_t = TableJeuDao().lister(joueur=None, seance=id_seance)
        if len(table_list_t) == int(os.environ["NB_JOUEURS_MAX_PAR_TABLE"]):
            resultat = "non table libre"
            return resultat

        # Mettre en place la gestion de table
        id_mj = mj.id_joueur
        resultat = TableJeuDao().gerer_par_mj(id_mj, id_seance, scenario, info_comple)
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
                         "niveau", "compétences", "langues parlées"]

        # liste de liste des persos de chaque table
        list_perso_des_tables = [t.liste_perso() for t in table_jeu]

        table_as_list = [t.as_list()[0:3] for t in table_jeu]
        print(table_as_list)

        i = 0
        for table in table_jeu:
            perso_as_list = [p.as_list()[1:7] for p in table.personnages]
            resultat_perso = tabulate(tabular_data=perso_as_list,
                                      headers=entetes_perso,
                                      tablefmt="psql",
                                      floatfmt=".2f") + "\n"
            print(resultat_perso)
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
