'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

import os

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage

from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao


class TableJeuService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer_table(self, id_seance):
        '''Service de création d'une Table de Jeu
        '''
        print("Service : Création de la TableJeu")
        table = TableJeu(id_table=None, id_seance=id_seance)
        TableJeuDao().creer(table)
        print("Service : Création de la TableJeu - Terminé")
        return table

    def trouver_par_id(self, id_table):
        print("Service : Trouver Table par id")
        table_jeu = TableJeuDao().trouver_par_id(id_table)
        print("Service : Trouver Table par id - Terminé")
        return table_jeu

    def lister_personnages(self, table_jeu) -> list[Personnage]:
        '''Lister les personnages d'une Table de Jeu
        '''
        print("Service : Lister personnages d'une table")
        liste_personnages = TableJeuDao().lister_personnages(table_jeu)
        print("Service : Lister personnages d'une table - Terminé")
        return liste_personnages

    def lister(self, joueur=None, seance=None, complete=None) -> list[TableJeu]:
        '''Retourne un liste de tables
        Params
        ------
        Si les paramètres sont à None, liste toutes les tables
        Params
        ------
        joueur : Joueur
            sélectionne uniquement les tables du joueur
            si None, sélectionne tous les joueurs
        seance : int
            sélectionne uniquement les tables de la séance
            si None, sélectionne toutes les seances
        complete : booleen
            si True, sélectionne uniquement les tables complètes
            si False, sélectionne uniquement les tables disponibles
            si None, sélectionne toutes les tables

        '''
        print("Service : Lister tables")
        liste_tables = TableJeuDao().lister(joueur, seance)

        if complete is False:
            for table in liste_tables:
                if not self.est_disponible(table):
                    liste_tables.pop(table)
        elif complete:
            for table in liste_tables:
                if self.est_disponible(table):
                    liste_tables.pop(table)

        print("Service : Lister tables - Terminé")
        return liste_tables

    def est_disponible(self, table):
        print("Service : Disponibilité Table")
        est_dispo = (TableJeuDao().nombre_joueurs_assis(table)
                     < int(os.environ["NB_JOUEURS_MAX_PAR_TABLE"]))
        print("Service : Disponibilité Table - Terminé")
        return est_dispo
