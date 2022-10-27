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
    '''
    Classe contenant les méthodes de service de MaitreJeu
    '''

    def lister_tables(self, mj):
        '''Service de listing de tables du mj
        '''
        print("Service : Listing de TableJeu du mj")

        table_list = MaitreJeuDao().lister_tables_mj(mj)

        print("Service : Listing de TableJeu du mj - Terminé")
        return table_list

    def quitter_table(self, mj, seance):
        '''Service de résiliation de tables du mj
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

    def gerer_table(self, id_seance, scenario, info_comple):
        '''Service de gerer une table pour mj
            return -> str
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
