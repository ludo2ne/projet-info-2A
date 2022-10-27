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

    def lister_par_joueur(self, joueur) -> list[Personnage]:
        '''lister des personnages d'une utilisateur

        Parameters:
        joueur: Joueur
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

    def trouver_par_id(self, id_personnage) -> Personnage:
        '''Trouver un personnage grace à son id
        Params
        ------
        id_personnage : int
            id du personnage recherché
        '''
        print("DAO : Trouver personnage par id")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM jdr.personnage "
                        " WHERE id_personnage = %(id_personnage)s;",
                        {"id_personnage": id_personnage})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        print(res)

        personnage = None
        if res:
            personnage = Personnage(id_personnage=res["id_personnage"],
                                    nom=res["nom"],
                                    classe=res["classe"],
                                    race=res["race"],
                                    niveau=res["niveau"])

        print("DAO : Trouver personnage par id - Terminé")

        return personnage

    def trouver_joueur(self, personnage) -> Joueur:
        '''trouver le joueur à qui appartient le personnage

        Parameters:
        personnage: Personnage
        '''
        print("DAO : Trouver joueur depuis personnage")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT j.* FROM jdr.joueur j "
                        " INNER JOIN jdr.personnage p USING(id_joueur) "
                        " WHERE p.id_personnage = %(id_personnage)s;",
                        {"id_personnage": personnage.id_personnage})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        joueur = None
        if res:
            joueur = Joueur(id_joueur=res["id_joueur"],
                            pseudo=res["pseudo"],
                            nom=res["nom"],
                            prenom=res["prenom"],
                            mail=res["mail"])

        print("DAO : Trouver joueur depuis personnage - Terminé")

        return joueur

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
                        "SELECT t.*                                             "
                        "  FROM jdr.personnage p                                "
                        "  JOIN jdr.table_personnage tp USING (id_personnage)   "
                        "  JOIN jdr.table_jeu t USING(id_table)                 "
                        "WHERE id_personnage=%(id_perso)s                       ",
                        {"id_perso": personnage.id_personnage})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        print("DAO : " + str(len(res)) +
              f" tables avec le personnage {personnage.nom}")

        print("DAO : Listing des tables d'un personnage - Terminé")

        # Pour l'instant, on ne retourne que le nombre de tables où
        # le personnage est présent. Si nécessaire, on pourra retourner la liste des tables
        return len(res)

    def quitter_table(self, personnage, table=None) -> bool:
        '''Suppression de la présence d'un personnage à une ou plusieurs tables

        TODO corriger méthode

        Parameters
        ----------
        * personnage : Personnage
            * le personnage à ajouter
        * table : TableJeu
            * la table de jeu que le personnage quitte
            * si non renseigné le personnage quitte toutes les tables

        Returns
        -------
        * True si l'opération est un succés
        * False sinon
        '''
        print("DAO : Suppression de la présence d'un personnage à une table")

        variables = {"id_perso": personnage.id_personnage}

        requete = "   DELETE                                      "\
            "           FROM jdr.table_personnage                 "\
            "          WHERE id_personnage = %(id_perso)s         "

        if table:
            requete += " AND id_table = %(id_table)s          "
            variables["id_table"] = table.id_table

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le personnage des tables où il est utilisé
                    cursor.execute(requete,
                                   variables)
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        if table:
            print("DAO : Personnage " + personnage.nom + " enlevé de la table")
        else:
            print("DAO : Personnage " + personnage.nom +
                  " enlevé de toutes les tables")

        print("DAO : Suppression de la présence d'un personnage à une table - Terminé")

        return [res > 0]

    def inscrire_table(self, table, personnage) -> bool:
        '''Inscription d'un personnage sur une table dans la base de données

        Parameters:
        table : int(id_table)
        personnage : Personnage
        '''
        print("DAO : Inscription d'un personnage sur une table")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.table_personnage(id_table,id_personnage) VALUES "
                        "(%(id_table)s,%(id_personnage)s) RETURNING id_table,id_personnage;",
                        {"id_table": table,
                         "id_personnage": personnage.id_personnage})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        inscrit = False
        if res:
            inscrit = True

        print("DAO : Inscription d'un personnage sur une table - Terminé")

        return [len(res) > 0]


# TODO fusionner avec inscrire_table

    def rejoindre_table(self, table, personnage) -> bool:
        '''Ajouter un personnage à une table de jeu
        Parameters
        ----------
        * personnage : Personnage
            * le personnage à ajouter
        * table : TableJeu
            * la table de jeu que le personnage rejoint
        '''
        print("DAO : Personnage rejoint une table")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le personnage des tables où il est utilisé
                    cursor.execute(
                        "INSERT INTO jdr.table_personnage            "
                        "VALUES(%(id_table)s,%(id_perso)s)           ",
                        {"id_table": table.id_table, "id_perso": personnage.id_personnage})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        print("DAO : Personnage qui rejoint une table - Terminé")

        return [res > 0]
