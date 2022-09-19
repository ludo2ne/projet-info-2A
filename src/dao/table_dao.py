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
        '''Creation d'un joueur dans la base de données

        Parameters
        ----------
        table : Table
        '''
        created = False

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                requete = "INSERT INTO jdr.table_jeu VALUES (%(numero)s);", {
                    "numero": table.numero}
                print(requete)
                cursor.execute(
                    "INSERT INTO jdr.table_jeu VALUES "
                    "(%(numero)s);", {"numero": table.numero})
                res = cursor.fetchone()
        if res:
            attack.id = res['id_attack']
            created = True
        return created

    def ajouter_joueur(self, joueur):
        '''
        Ajoute un joueur à une table
        '''
        print("INSERT INTO table_joueurs VALUES...")
