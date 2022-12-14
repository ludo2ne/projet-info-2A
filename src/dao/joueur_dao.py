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
from view.session import Session

from business_object.joueur import Joueur
from business_object.maitre_jeu import MaitreJeu
from business_object.personnage import Personnage

from dao.personnage_dao import PersonnageDao


class JoueurDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de dao de Joueur

    Attributes
    ----------
    None

    Methods
    -------
    creer(joueur : Joueur) : bool
    trouver_par_id(id_joueur : int) : Joueur
    trouver_par_pseudo(pseudo : str) : Joueur
    rejoindre_table(table : TableJeu, joueur : Joueur, personnage : Personnage) : bool
    lister_tables(joueur : Joueur) : bool
    supprimer_compte(compte : Joueur) : bool
    lister_tous() : list[Joueur]


    '''

    def creer(self, joueur) -> bool:
        '''Creation d'un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        '''
        print("DAO : Création d'un joueur")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.joueur(pseudo, nom, prenom, mail, est_mj) VALUES "
                        "(%(pseudo)s,%(nom)s,%(prenom)s,%(mail)s, false) RETURNING id_joueur;",
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

        print("DAO : Création d'un joueur - Terminé")

        return created

    def trouver_par_id(self, id_joueur) -> Joueur:
        '''trouver un joueur grace à son id

        Parameters
        ----------
        id_joueur : int
            numéro id du joueur que l'on souhaite trouver

        Returns
        -------
        joueur : Joueur
            renvoie le joueur que l'on cherche par id
        '''
        print("DAO : Trouver joueur par id")

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
            joueur = Joueur(pseudo=res["pseudo"],
                            nom=res["nom"],
                            prenom=res["prenom"],
                            mail=res["mail"],
                            id_joueur=res["id_joueur"])

            # Si ce n est pas un simple joueur mais un Maitre du Jeu
            if res["est_mj"]:
                joueur = MaitreJeu(joueur)

        print("DAO : Trouver joueur par id - Terminé")

        return joueur

    def trouver_par_pseudo(self, pseudo) -> Joueur:
        '''trouver un joueur grace à son pseudo

        Parameters
        ----------
        pseudo : str
            pseudo du joueur que l'on souhaite trouver

        Returns
        -------
        joueur : Joueur
            renvoie le joueur recherché par pseudo
        '''
        print("DAO : Trouver joueur par pseudo")

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
                            id_joueur=res["id_joueur"])

            # Si ce n est pas un simple joueur mais un Maitre du Jeu
            if res["est_mj"]:
                joueur = MaitreJeu(joueur)

        print("DAO : Trouver joueur par pseudo - Terminé")

        return joueur

    def rejoindre_table(self, table, joueur, personnage) -> bool:
        '''Ajoute un joueur à une table        

        Parameters
        ----------
        table : Table
            table sur laquelle ajouter le joueur
        joueur : Joueur
            joueur à ajouter
        personnage : Personnage
            personnage choisi par le joueur

        Returns
        -------
        inserted : bool
            succès d'ajout du personnage du joueur sur la table
        '''

        print("DAO : Rejoindre une table")

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

        print("DAO : Rejoindre une table - Terminé")

        return inserted

    def lister_tables(self, joueur) -> dict:
        '''Lister les tables où un joueur est assis dans la base de données

        Parameters
        ----------
        joueur : Joueur
            joueur dont on veut lister les tables sur lesquelles il est inscrit

        Returns
        -------
        res : dict
            dictionnaire qui rescence des tables du joueurs
        '''
        print("DAO : Listing des tables d'un joueur")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Lister les tables du personnage
                    cursor.execute(
                        "SELECT id_table,id_seance FROM jdr.personnage "
                        "JOIN jdr.table_personnage USING (id_personnage)"
                        "JOIN jdr.table_jeu USING(id_table)"
                        "WHERE id_joueur=%(id_joueur)s",
                        {"id_joueur": joueur.id_joueur})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        print("DAO : " + str(len(res)) +
              f" tables avec le joueur {joueur.pseudo}")

        print("DAO : Listing des tables d'un joueur - Terminé")

        return (res)

    def supprimer_compte(self, compte) -> bool:
        '''Suppression du compte d'un joueur 
        dans la base de données

        Parameters
        ----------
        compte : Joueur
            compte du joueur à supprimer de la base de donnée

        Returns
        -------
        [res > 0] : bool
            True si le personnage a bien été supprimé
        '''
        print("DAO : Suppression du compte d'un joueur")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un joueur
                    cursor.execute(
                        "DELETE FROM jdr.joueur "
                        "WHERE id_joueur=%(id_compte)s",
                        {"id_compte": compte.id_joueur})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        print("DAO : Suppression de compte- Terminé")

        return [res > 0]

    def lister_tous(self) -> list[Joueur]:
        '''lister tous les joueurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_joueurs : list[Joueur]
            renvoie la liste de tous les joueurs dans la base de données
        '''
        print("DAO : Lister tous les joueurs")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                   "
                        "   FROM jdr.joueur         "
                        "  WHERE pseudo != 'admin'  ")
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        liste_joueurs = []
        if res:
            for row in res:
                joueur = Joueur(pseudo=row["pseudo"],
                                nom=row["nom"],
                                prenom=row["prenom"],
                                mail=row["mail"],
                                id_joueur=row["id_joueur"])
                liste_est_mj = row["est_mj"]

                # liste_joueurs une liste
                liste_joueurs.append([liste_est_mj, joueur])

        print("DAO : Lister tous les joueurs - Terminé")

        return liste_joueurs
