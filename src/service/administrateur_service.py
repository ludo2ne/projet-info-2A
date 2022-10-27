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

from view.session import Session

from business_object.joueur import Joueur
from business_object.personnage import Personnage
from business_object.table_jeu import TableJeu

from dao.joueur_dao import JoueurDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao


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

        sceance_courante = None
        table_txt = ""

        for t in liste_tables:

            # Si on est dans une nouvelle seance
            if t.id_seance != sceance_courante or not sceance_courante:
                sceance_courante = t.id_seance
                table_txt += "\n###########################################################"
                table_txt += "\nSéance " + str(sceance_courante)
                table_txt += "\n###########################################################\n"

            table_txt += "\nTable " + str(t.id_table)
            table_txt += "\n-------\n\n"

            if t.maitre_jeu:
                table_txt += "Maître du jeu : " + t.maitre_jeu.pseudo + "\n"
                table_txt += "Scénario : " + t.scenario + "\n"

            if t.personnages != []:
                entetes = ["id", "Nom", "Classe",
                           "Race", "Niveau", "Joueur"]
                personnages_as_list = [p.as_list() for p in t.personnages]

                for p in personnages_as_list:
                    current_perso = PersonnageDao().trouver_par_id(p[0])
                    joueur = PersonnageDao().trouver_joueur(current_perso)
                    p.append(joueur.prenom + " " + joueur.nom +
                             " (" + joueur.pseudo + ")")

                table_txt += "Liste des personnages :\n" + tabulate(tabular_data=personnages_as_list,
                                                                    headers=entetes,
                                                                    tablefmt="psql",
                                                                    floatfmt=".2f") + "\n"

        print("Service : Voir programme complet - Terminé")

        resultat += table_txt

        return resultat

    def lister_tables_actives(self) -> list[TableJeu]:
        '''Retourne la liste de toutes les tables de jeu
        '''

        print("Service : Lister les tables actives")
        liste_tables = TableJeuDao().lister_tables_actives()
        print("Service : Lister les tables actives - Terminé")

        return liste_tables

    def supprimer_table(self):
        '''TODO corriger
        '''
        liste_tables = TableJeuDao().lister(self)
        table_couple = []
        for k in range(len(liste_tables)):
            table_couple.append(
                [TableJeuDao().nombre_joueurs_assis(liste_tables[k]), liste_tables[k]])
            if table_couple[k][0] == 0:
                TableJeuDao().supprimer_table(table_couple[k][1])
        return table_couple
