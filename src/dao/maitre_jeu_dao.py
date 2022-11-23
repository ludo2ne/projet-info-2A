'''
Module maitre_jeu_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from typing import List, Optional

from dao.db_connection import DBConnection
from utils.singleton import Singleton

from view.session import Session

from business_object.maitre_jeu import MaitreJeu


class MaitreJeuDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de dao de MaitreJeu
    '''

    def resilier_table(self, mj, seance) -> bool:
        '''Suppression de la présence d'un maitre du jeu à une table 
        dans la base de données

        Parameters
        ----------
        mj : MaitreJeu
        seance:integer
        '''
        print("DAO : Suppression de la présence d'un maitre du jeu à une table")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le maitre du jeu de la table choisie
                    cursor.execute(
                        "UPDATE jdr.table_jeu                           "
                        "   SET id_maitre_jeu = null,                   "
                        "       scenario = null,                        "
                        "       infos_complementaires = null            "
                        " WHERE id_maitre_jeu = %(id_maitre_jeu)s       "
                        "   AND id_seance = %(id_seance)s               ",
                        {"id_maitre_jeu": mj.id_joueur, "id_seance": seance})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise
        print("DAO : Maitre du jeu enlevé de " + str(res) + " table(s)")

        print("DAO : Suppression de la présence d'un maitre du jeu à une table - Terminé")

        return [res > 0]

    def lister_tables_mj(self, mj) -> list:
        '''Lister les tables où un maitre du jeu est assis dans la base de données

        Parameters
        ----------
        mj : maitre du jeu
        '''
        print("DAO : Listing des tables d'un maitre du jeu")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Lister les tables du maitre du jeu
                    cursor.execute(
                        "SELECT id_table,                           "
                        "       id_seance,                          "
                        "       scenario                            "
                        "  FROM jdr.table_jeu                       "
                        " WHERE id_maitre_jeu = %(id_mj)s           ",
                        {"id_mj": mj.id_joueur})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        print("DAO : " + str(len(res)) +
              f" tables avec le maitre du jeu {mj.prenom} {mj.nom}")
        table_list = []
        if res:
            for el in res:
                table_list.append(
                    [el["id_table"], el["id_seance"], el["scenario"]])

        print("DAO : Listing des tables d'un maitre du jeu - Terminé")

        return table_list

    def devenir_mj(self) -> bool:
        '''Donner le statut mj à un joueur dans la base de données

        Parameters
        ----------
        None

        Returns
        -------
        bool :
            True si la mise à jour est réussie
            False sinon

        '''
        print("DAO : Accéder au statut maitre du jeu")

        joueur = Session().user
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Passer à true la valeur est_mj pour devenir maitre du jeu
                    cursor.execute(
                        "UPDATE jdr.joueur                    "
                        "   SET est_mj = true                 "
                        " WHERE id_joueur=%(id_joueur)s       ",
                        {"id_joueur": joueur.id_joueur})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        print("DAO : Accéder au statut maitre du jeu - Terminé")

        return (res > 0)
