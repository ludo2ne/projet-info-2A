'''
Module table_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.table import Table
from typing import List, Optional
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class TableDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer(self, table) -> bool:
        '''Création d'une table dans la base de données

        Parameters
        ----------
        table : Table
            la table à créer
        '''
        inserted = False

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO jdr.table_jeu(numero) VALUES "
                    "(%(numero)s) RETURNING id_table;", {"numero": table.numero})
                print(cursor.description)
                res = cursor.fetchone()
        if res:
            table.id = res['id_table']
            inserted = True
        return inserted

    def ajouter_joueur(self, table, joueur):
        '''Ajoute un joueur à une table        

        Parameters
        ----------
        table : Table
            table sur laquelle ajouter le joueur
        joueur : Joueur
            joueur à ajouter
        '''
        inserted = False

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO jdr.table_joueur(id_table, id_joueur) VALUES "
                    "(%(id_table)s, %(id_joueur)s) RETURNING id_table;", {"id_table": table.id, "id_joueur": joueur.id})
                print(cursor.description)
                res = cursor.fetchone()
        if res:
            inserted = True
        return inserted

    def nombre_joueurs_assis(self, table) -> int:
        '''Nombre de joueurs assis actuellement à la table
        '''
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT count(1) FROM jdr.table_joueur WHERE id_table = "
                    "%(id_table)s;", {"id_table": table.id})
                print(cursor.description)
                nb_joueurs = cursor.fetchone() TODO
        return nb_joueurs
