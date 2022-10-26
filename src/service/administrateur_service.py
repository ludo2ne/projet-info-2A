'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

import os
from tabulate import tabulate
from typing import List, Optional

from business_object.joueur import Joueur
from business_object.personnage import Personnage
from dao.joueur_dao import JoueurDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from view.session import Session


class AdministrateurService():

    def creer_table_autorisee(self, seance) -> bool:
        '''Dit si le joueur n'a pas atteint le nombre maximum de Personnages
        '''
        print("Service : Creer table autorisee")
        nb_tables = TableJeuDao().compter_tables_par_seance(seance)
        print(nb_tables)
        return nb_tables < int(os.environ["NB_TABLES_MAX_PAR_SEANCE"])

    def voir_programme_complet(self):

        print("Service : Voir programme complet")

        liste_tables = TableJeuDao().lister()

        entetes = ["Séance", "Numéro", "Scénario",
                   "Maître du Jeu"]

        tables_as_list = [t.as_list() for t in liste_tables]

        resultat = "Liste des tables \n" + tabulate(tabular_data=tables_as_list,
                                                    headers=entetes,
                                                    tablefmt="psql",
                                                    floatfmt=".2f") + "\n"

        print("Service : Voir programme complet - Terminé")

        return resultat
