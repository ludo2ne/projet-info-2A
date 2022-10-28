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

from business_object.message import Message


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
                         "contenu": texte})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        created = False
        if res == 1:
            created = True

        print("DAO : Création d'un message - Terminé")

        return created

    def lister_par_joueur(self, joueur):
        '''lister les messages envoyés à un utilisateur
        '''
        print("DAO : lister les messages envoyés à un utilisateur")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM jdr.message "
                        " WHERE id_joueur = %(id)s;",
                        {"id": joueur.id_joueur})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        # recuperer les messages en les sauvgardant dans une liste messages
        messages = []
        if res:
            for row in res:
                msg = Message(id_message=row["id_message"],
                              id_joueur=row["id_joueur"],
                              contenu=row["contenu"],
                              lu=row["lu"],
                              date_creation=row["date_creation"])
                messages.append(msg)
            # print("recuperer data ok")
            # mettre a jour le statut de l'attribut lu des objets messages correspondants
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE jdr.message "
                        " SET lu=True WHERE id_joueur = %(id)s;",
                        {"id": joueur.id_joueur})
            # print("mettre a jour ok")

        print("DAO : Voir les messages du joueur - Terminé")

        return messages
