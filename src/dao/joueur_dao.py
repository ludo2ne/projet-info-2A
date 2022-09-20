'''
Module joueur_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from typing import List, Optional

from dao.db_connection import DBConnection
from utils.singleton import Singleton

from business_object.joueur import Joueur


class JoueurDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de dao de Joueur
    '''

    def creer(self, joueur) -> bool:
        '''Creation d'un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur
        '''

        print("Sauvegarde d'un joueur en BDD")

        created = False

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO jdr.joueur(nom, prenom) VALUES "
                    "(%(nom)s,%(prenom)s) RETURNING id_joueur;", {"nom": joueur.nom, "prenom": joueur.prenom})
                print(cursor.description)
                res = cursor.fetchone()
        if res:
            joueur.id = res['id_joueur']
            created = True
        return created

    def lister_tous(self):
        '''
        Liste de tous les joueurs
        '''
        print("SELECT * FROM joueur")
