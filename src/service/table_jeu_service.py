'''
Module table_jeu_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

import os
from tabulate import tabulate

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage
from business_object.maitre_jeu import MaitreJeu

from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from dao.joueur_dao import JoueurDao


class TableJeuService:
    '''Classe contenant les méthodes de service de Joueur

    Attributes
    ----------
    None

    Methods
    -------
    creer(id_seance : int) : TableJeu
    supprimer() : list
    trouver_par_id(id_table : int) : TableJeu
    lister_personnages(table_jeu : TableJeu) : list[Personnage]
    lister(joueur=None : Joueur, seance=None : int, complete=None : bool) : list[TableJeu]
    est_disponible(table) : bool
    affichage_liste(liste_tables : list[TableJeu]) : str
    trouver_mj(table) : MaitreJeu

    '''

    def creer(self, id_seance) -> TableJeu:
        '''Service de création d'une Table de Jeu

        Params
        ------
        * id_seance : int
            * le numéro de la séance

        Returns
        -------
        La Table de Jeu créée
        '''
        print("Service : Création de la TableJeu")
        table = TableJeu(id_table=None, id_seance=id_seance)
        TableJeuDao().creer(table)
        print("Service : Création de la TableJeu - Terminé")
        return table

    def supprimer(self) -> list:
        ''' Supprimer toutes les tables sans joueur ni MJ
        '''

        print("Service : Supprimer table")

        liste_tables = TableJeuDao().lister()
        table_couple = []
        statut_suppression_global = True
        for k in range(len(liste_tables)):
            table_couple.append(
                [TableJeuDao().nombre_joueurs_assis(liste_tables[k]), liste_tables[k]])
            if table_couple[k][0] == 0 and table_couple[k][1].maitre_jeu is None:
                statut_suppression_table = TableJeuDao(
                ).supprimer(table_couple[k][1])
                statut_suppression_global = statut_suppression_table and statut_suppression_global

        print("Service : Supprimer table - Terminé")

        return statut_suppression_global

    def trouver_par_id(self, id_table) -> TableJeu:
        '''Service pour trouver une Table de Jeu à partir de son id

        Params
        ------
        * id_table : int
            * l'identifiant de la table

        Returns
        -------
        La Table de Jeu
        '''
        print("Service : Trouver Table par id")
        table_jeu = TableJeuDao().trouver_par_id(id_table)
        print("Service : Trouver Table par id - Terminé")
        return table_jeu

    def lister_personnages(self, table_jeu) -> list[Personnage]:
        '''Lister les personnages d'une Table de Jeu

        Params
        ------
        * table_jeu : TableJeu
            * la Table de Jeu

        Returns
        -------
        La liste de personnages de la Table de Jeu
        '''
        print("Service : Lister personnages d'une table")
        liste_personnages = TableJeuDao().lister_personnages(table_jeu)
        print("Service : Lister personnages d'une table - Terminé")
        return liste_personnages

    def lister(self, joueur=None, seance=None, complete=None) -> list[TableJeu]:
        '''Retourne une liste de tables
        Si les paramètres sont à None, liste toutes les tables

        Params
        ------
        * joueur : Joueur
            * sélectionne uniquement les tables du joueur
            * si None, sélectionne tous les joueurs
        * seance : int
            * sélectionne uniquement les tables de la séance
            * si None, sélectionne toutes les seances
        * complete : booleen
            * si True, sélectionne uniquement les tables complètes
            * si False, sélectionne uniquement les tables disponibles
            * si None, sélectionne toutes les tables

        Returns
        -------
        Une liste de Tables de Jeu
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

    def est_disponible(self, table) -> bool:
        '''Teste si il y a des places libre à la Table de Jeu

        Params
        ------
        * table : TableJeu
            * la table de jeu à tester

        Returns
        -------
        * True si il y a encore des places libres 
        * False si la table est complète
        '''
        print("Service : Disponibilité Table")
        est_dispo = (TableJeuDao().nombre_joueurs_assis(table)
                     < int(os.environ["NB_JOUEURS_MAX_PAR_TABLE"]))
        print("Service : Disponibilité Table - Terminé")
        return est_dispo

    def affichage_liste(self, liste_tables) -> str:
        '''Convertir une liste de Table de Jeu en String pour afficher sous forme de tableau
        Params
        ------
        * liste_tables : list[TableJeu]
            * une liste de Tables de Jeu

        Returns
        -------
        une chaine de caractères mise en forme de tableau pour affichage
        '''

        print("Service : Affichage liste de tables")

        entetes = ["Séance", "Numéro", "Scénario",
                   "Maître du Jeu"]

        tables_as_list = [t.as_list() for t in liste_tables]

        resultat = "Liste des tables \n" + tabulate(tabular_data=tables_as_list,
                                                    headers=entetes,
                                                    tablefmt="psql",
                                                    floatfmt=".2f") + "\n"

        print("Service : Affichage liste de tables - Terminé")

        return resultat

    def trouver_mj(self, table) -> MaitreJeu:
        '''Service pour trouver le Maitre du Jeu d'une Table

        Params
        ------
        * table : tableJeu
            * la table sur laquelle on souhaite connaitre le MJ

        Returns
        -------
        Le Maître du Jeu ou None s'il n'y a pas de Maître du Jeu à la Table
        '''
        print("Service : Trouver Maitre du Jeu de la Table")
        id_maitre_jeu = TableJeuDao().trouver_mj(table)
        maitre_jeu = JoueurDao().trouver_par_id(id_maitre_jeu)
        print("Service : Trouver Maitre du Jeu de la Table - Terminé")
        return maitre_jeu
