'''
Module table_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.table_jeu import TableJeu
from typing import List, Optional
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class TableJeuDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer(self, table) -> bool:
        '''Création d'une table dans la base de données

        Parameters
        ----------
        table : TableJeu
            la table de jeu à créer
        '''
        inserted = False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.table_jeu(numero) VALUES "
                        "(%(numero)s) RETURNING id_table;", {"numero": table.numero})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        if res:
            table.id = res['id_table']
            inserted = True
        return inserted

    def trouver_par_id(self, id_table) -> int:
        '''Obtenir une table à partir de son id_table
        '''
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM jdr.table WHERE id_table = "
                        "%(id_table)s;", {"id_table": id_table})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        table = None
        if res:

            # TODO trouver mj

            table = TableJeu(id_table=res['id_table'],
                             numero=res['numero'],
                             scenario=res['scenario'])

            table.liste_personnages = lister_personnages(table)

        return table

    def lister_personnages(self, table):
        '''retourne la liste des personnages de la table
        '''
        # TODO
        return null

    def nombre_joueurs_assis(self, table) -> int:
        '''Nombre de joueurs assis actuellement à la table
        '''
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT count(1) FROM jdr.table_joueur WHERE id_table = "
                        "%(id_table)s;", {"id_table": table.id})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        nb_joueurs = res['count']
        return nb_joueurs
