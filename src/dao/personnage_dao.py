'''
Module personnage_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 14/10/2022
Licence : Domaine public
Version : 1.0
'''

from typing import List, Optional

from dao.db_connection import DBConnection
from utils.singleton import Singleton
from view.session import Session

from business_object.joueur import Joueur
from business_object.personnage import Personnage


class PersonnageDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de dao de Personnage
    '''

    def creer(self, personnage) -> bool:
        '''Creation d'un personnage dans la base de données

        Parameters
        ----------
        personnage : Personnage
        '''
        print("DAO : Création d'un personnage")

        joueur = Session().user

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.personnage(nom, race, classe, niveau, id_joueur) VALUES "
                        "(%(nom)s,%(race)s,%(classe)s,%(niveau)s,%(id_joueur)s) RETURNING id_personnage;",
                        {"nom": personnage.nom,
                         "race": personnage.race,
                         "classe": personnage.classe,
                         "niveau": personnage.niveau,
                         "id_joueur": joueur.id_joueur})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        created = False
        if res:
            personnage.id = res['id_personnage']
            created = True

        print("DAO : Création d'un personnage - Terminé")

        return created

    def lister_par_joueur(self, joueur):
        '''lister des personnages d'une utilisateur
        '''
        print("DAO : Lister personnage du joueur")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM jdr.personnage "
                        " WHERE id_joueur = %(id)s;",
                        {"id": joueur.id_joueur})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        personnages = []
        if res:
            for row in res:
                perso = Personnage(id_personnage=row["id_personnage"],
                                   nom=row["nom"],
                                   classe=row["classe"],
                                   race=row["race"],
                                   niveau=row["niveau"])
                personnages.append(perso)
        # Implemente la liste des personnages dans le profil joueur
        joueur.liste_personnages = personnages
        print("DAO : Lister personnage du joueur - Terminé")

        return personnages

    def supprimer(self, personnage) -> bool:
        '''Suppression d'un personnage dans la base de données

        Parameters
        ----------
        personnage : Personnage
        '''
        print("DAO : Suppression d'un personnage")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le personnage
                    cursor.execute(
                        "DELETE FROM jdr.personnage "
                        "WHERE id_personnage=%(id_perso)s",
                        {"id_perso": personnage.id_personnage})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise
        print("DAO : " + str(res) + " Personnage supprimé")

        print("DAO : Suppression d'un personnage - Terminé")

        return [res > 0]

    def lister_tables(self, personnage) -> bool:
        '''Lister les tables où un personnage est utilisé dans la base de données

        Parameters
        ----------
        personnage : Personnage
        '''
        print("DAO : Listing des tables d'un personnage")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Lister les tables du personnage
                    cursor.execute(
                        "SELECT id_table,id_seance FROM jdr.personnage "
                        "JOIN jdr.table_personnage USING (id_personnage)"
                        "JOIN jdr.table_jeu USING(id_table)"
                        "WHERE id_personnage=%(id_perso)s",
                        {"id_perso": personnage.id_personnage})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        print("DAO : " + str(len(res)) + " tables avec ce personnage")

        print("DAO : Listing des tables d'un personnage - Terminé")

        # Pour l'instant, on ne retourne que le nombre de tables où
        # le personnage est présent. Si nécessaire, on pourra retourner la liste des tables
        return len(res)
