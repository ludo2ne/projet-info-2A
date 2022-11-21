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

    def supprimer_par_joueur(self, joueur):
        '''Supprimer les messages d'un joueur

         Parameters
         ----------
         joueur : Joueur
             Le joueur pour lequel on doit supprimer les messages

         Returns
         -------
         boolean : 
             True si la suppression s'est bien déroulée
             False sinon
         '''
        print("DAO : Suppression des messages d'un joueur")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM jdr.message                     "
                        " WHERE id_joueur = %(id_joueur)s            ",
                        {"id_joueur": joueur.id_joueur})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        print("DAO : Suppression des messages d'un joueur - Terminé")

        return res >= 0

    def lister_par_joueur(self, joueur, lu=True):
        '''lister les messages envoyés à un utilisateur
        '''
        print("DAO : lister les messages envoyés à un utilisateur")

        variables = dict()
        requete = "SELECT *                          "\
            "  FROM jdr.message                "\
            " WHERE id_joueur = %(id)s         "
        variables["id"] = joueur.id_joueur

        if lu == False:
            requete += " AND lu = %(statut_lu)s                   "
            variables["statut_lu"] = lu

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(requete, variables)
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
            if lu == True:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE jdr.message                     "
                            "   SET lu = True                       "
                            " WHERE id_joueur = %(id)s              ",
                            {"id": joueur.id_joueur})
            # print("mettre a jour ok")

        print("DAO : Voir les messages du joueur - Terminé")

        return messages

    def lister_admin(self, admin, lu=True):
        '''lister les messages envoyés à un utilisateur
        '''
        print("DAO : lister les messages envoyés à un utilisateur")

        variables = dict()
        requete = "SELECT *                          "\
            "  FROM jdr.message                "\
            " WHERE id_joueur = %(id)s         "
        variables["id"] = admin.id_admin

        if lu == False:
            requete += " AND lu = %(statut_lu)s                   "
            variables["statut_lu"] = lu

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(requete, variables)
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
            if lu == True:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE jdr.message               "
                            "   SET lu = True                 "
                            " WHERE id_joueur = %(id)s        ",
                            {"id": admin.id_admin})
            # print("mettre a jour ok")

        print("DAO : Voir les messages du joueur - Terminé")

        return messages
