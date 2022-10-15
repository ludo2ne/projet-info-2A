'''
Module message_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from typing import List, Optional

from dao.db_connection import DBConnection
from utils.singleton import Singleton
from view.session import Session

from business_object.joueur import Joueur


class MessageDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de dao de Message
    '''

    def creer(self, joueur, texte) -> bool:
        '''Création d'un message dans la base de données

        Parameters
        ----------
        joueur : Joueur
        texte : str
        '''
        print("DAO : Création d'un message")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.message(id_joueur, date_creation, contenu, lu) VALUES "
                        "(%(id_joueur)s, current_timestamp ,%(contenu)s, false) RETURNING id_message;",
                        {"id_joueur": joueur.id_joueur,
                         "contenu": contenu})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        created = False
        if res:
            created = True

        print("DAO : Création d'un message - Terminé")

        return created

    def lister_par_joueur(self, joueur):
        '''Liste des messages d'un joueur

        Parameters
        ----------
        joueur : Joueur
        '''
        pass
        # TODO
