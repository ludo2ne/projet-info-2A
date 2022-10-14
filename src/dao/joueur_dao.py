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
        print("Création d'un joueur en BDD")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.joueur(pseudo, nom, prenom, mail) VALUES "
                        "(%(pseudo)s,%(nom)s,%(prenom)s,%(mail)s) RETURNING id_joueur;",
                        {"pseudo": joueur.pseudo,
                         "nom": joueur.nom,
                         "prenom": joueur.prenom,
                         "mail": joueur.mail})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        created = False
        if res:
            joueur.id = res['id_joueur']
            created = True
        return created

    def trouver_par_id(self, id_joueur) -> Joueur:
        '''trouver un joueur grace à son id
        '''
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM jdr.joueur "
                        " WHERE id_joueur = %(id_joueur)s;",
                        {"id_joueur": id_joueur})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        joueur = None
        if res:
            joueur = Joueur(pseudo=res['pseudo'],
                            nom=res['nom'],
                            prenom=res['prenom'],
                            mail=res['mail'],
                            id_joueur=res['id_joueur'])

            # TODO
            # joueur.liste_personnage = lister_personnages(joueur)

        return joueur

    def trouver_par_pseudo(self, pseudo) -> Joueur:
        '''trouver un joueur grace à son pseudo
        '''
        print("INFO : JoueurDao.trouver_par_pseudo({})".format(pseudo))

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM jdr.joueur "
                        " WHERE pseudo = %(pseudo)s;",
                        {"pseudo": pseudo})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        joueur = None
        if res:
            joueur = Joueur(pseudo=res["pseudo"],
                            nom=res["nom"],
                            prenom=res["prenom"],
                            mail=res["mail"],
                            id=res["id_joueur"])

            # TODO
            # joueur.liste_personnage = lister_personnages(joueur)

        return joueur

    def rejoindre_table(self, table, joueur, personnage):
        '''Ajoute un joueur à une table        

        Parameters
        ----------
        table : Table
            table sur laquelle ajouter le joueur
        joueur : Joueur
            joueur à ajouter
        personnage : Personnage
            personnage choisi par le joueur
        '''
        inserted = False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.table_joueur(id_table, id_joueur, id_personnage) VALUES "
                        "(%(id_table)s, %(id_joueur)s, %(id_personnage)s) RETURNING id_table;",
                        {"id_table": table.id, "id_joueur": joueur.id, "id_personnage": personnage.id})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        if res:
            inserted = True
        return inserted
