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
    resilier_table(mj : Joueur, seance : int): list
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

    def resilier_table(self, mj, id_seance) -> list:
        '''Service de résiliation de tables du mj

        Parameters
        ----------
        mj : Joueur
            le maître du jeu
        id_seance : int
            identifiant de la séance

        Returns
        -------
        list
        '''
        print("Service : Résiliation de TableJeu du mj")

        # Creation d'un dictionnaire id_seance --> description_seance
        dict_seance = SeanceDao().lister_toutes(dict=True)

        # instanciation de la table à supprimer
        table_correspondante = TableJeuDao().lister(mj=mj, seance=id_seance)[0]
        # Liste des joueurs assis à cette table
        joueur_list = TableJeuDao().joueurs_assis(table_correspondante)

        statut_resilier_table = MaitreJeuDao().resilier_table(mj, id_seance)
        err_message = ""
        if not statut_resilier_table:
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
        return [statut_resilier_table, err_message]

    def gerer_table(self, seance, scenario, infos_complementaires, mj=None, table=None) -> str:
        '''Service de gerer une table pour mj

        Parameters
        ----------
        seance : Seance
            Séance concernée
        scenario : str
            nom du scénario
        infos_complementaires : str
            informations complémentaires
        mj : MaitreJeu
            le Maitre du Jeu qui doit gerer la table

        Returns
        -------
        resultat : str
        '''
        print("Service : Gestion d'une table jeu du mj")
        if not mj:
            mj = Session().user

        if table:
            # Si une table a ete donnee en parametre
            table_jeu = table
        else:
            # Sinon on cherche une table libre pour la seance
            liste_tables_jeu = TableJeuDao().tables_sans_maitre_du_jeu(seance)
            # on prend la premiere table de la liste
            table_jeu = liste_tables_jeu[0]

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

        dict_seance = SeanceDao().lister_toutes(dict=True)

        # Liste des tables avec joueur comme mj
        table_jeu = TableJeuDao().lister(mj=joueur)

        entetes = ["séance", "id_table", "scénario", "Personnages"]

        entetes_perso = ["nom", "classe", "race",
                         "niveau", "competence", "langue_parlée"]

        # liste de liste des persos de chaque table
        list_perso_des_tables = [t.liste_perso() for t in table_jeu]

        # Préparation de l'affichage
        table_as_list = [t.as_list()[0:len(entetes)-1] for t in table_jeu]
        for el in table_as_list:
            el[0] = dict_seance[str(el[0])]

        # Affichage des personnages sur chaque table
        i = 0
        for table in table_jeu:
            perso_as_list = [p.as_list()[1:len(entetes_perso)+1]
                             for p in table.personnages]
            resultat_perso = tabulate(tabular_data=perso_as_list,
                                      headers=entetes_perso,
                                      tablefmt="psql",
                                      floatfmt=".2f") + "\n"
            # Affichage de la table (tableaux imbriqués)
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

    def liste_tables_sans_mj(self, seance) -> list[TableJeu]:
        '''Service pour lister les tables sans MJ pour une seance
        '''
        print("Service : Liste tables sans mj")
        liste_tables = TableJeuDao().tables_sans_maitre_du_jeu(seance)
        print("Service : Liste tables sans mj - Terminé")
        return liste_tables
