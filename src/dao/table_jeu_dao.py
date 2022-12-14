'''
Module table_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from typing import List, Optional
from dao.db_connection import DBConnection
from utils.singleton import Singleton

from dao.joueur_dao import JoueurDao
from dao.personnage_dao import PersonnageDao

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage
from business_object.joueur import Joueur


class TableJeuDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de dao de TableJeu
    '''

    def creer(self, table) -> bool:
        '''Création d'une table dans la base de données

        Parameters
        ----------
        table : TableJeu
            la table de jeu à créer
        '''

        print("DAO : Création d'une TableJeu")

        created = False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO jdr.table_jeu(id_seance) VALUES "
                        "(%(id_seance)s) RETURNING id_table;", {"id_seance": table.id_seance})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        if res:
            table.id_table = res['id_table']
            created = True

        print("DAO : Création d'une TableJeu - Terminé")

        return created

    def supprimer(self, table) -> bool:
        '''Suppression d'une Table de Jeu

        Parameters
        ----------
        table : TableJeu
            la Table de Jeu a supprimer

        Returns
        -------
        True si la suppression s'est bien passée
        False sinon

        '''
        print("DAO : Suppression d'une TableJeu")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE                                            "
                        "  FROM jdr.table_jeu                              "
                        " WHERE id_table = %(id_table)s                    ",
                        {"id_table": table.id_table})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        statut = (res == 1)
        print("DAO : Suppression d'une TableJeu - Terminé")

        return statut

    def trouver_par_id(self, id_table) -> TableJeu:
        '''Obtenir une table à partir de son id_table
        '''

        print("DAO : Trouver TableJeu par id")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                         "
                        "  FROM jdr.table_jeu             "
                        " WHERE id_table = %(id_table)s   ",
                        {"id_table": id_table})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        table = None
        if res:

            maitre_jeu = JoueurDao().trouver_par_id(res["id_maitre_jeu"])

            table = TableJeu(id_table=res['id_table'],
                             id_seance=res['id_seance'],
                             maitre_jeu=maitre_jeu,
                             scenario=res['scenario'],
                             infos_complementaires=res['infos_complementaires'])

            table.personnages = self.lister_personnages(table)

        print("DAO : Trouver TableJeu par id - Terminé")

        return table

    def lister_personnages(self, table):
        '''retourne la liste des personnages de la table
        '''
        print("DAO : Lister personnage d'une table")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT p.*                                             "
                        "  FROM jdr.personnage p                                "
                        " INNER JOIN jdr.table_personnage USING(id_personnage)  "
                        " INNER JOIN jdr.table_jeu t USING(id_table)            "
                        " WHERE t.id_table = %(id_table)s;                      ",
                        {"id_table": table.id_table})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        liste_personnages = []
        if res:
            for row in res:
                perso = Personnage(id_personnage=row["id_personnage"],
                                   nom=row["nom"],
                                   classe=row["classe"],
                                   race=row["race"],
                                   niveau=row["niveau"],
                                   competence=row["competence"],
                                   langues_parlees=row["langues_parlees"])
                liste_personnages.append(perso)

        print("DAO : Lister personnage d'une table - Terminé")

        return liste_personnages

    def nombre_joueurs_assis(self, table) -> int:
        '''Nombre de joueurs assis actuellement à la table
        '''
        print("DAO : Nombre de joueurs assis à une TableJeu")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT count(1)                                   "
                        "  FROM jdr.table_personnage                       "
                        " WHERE id_table = %(id_table)s                    ",
                        {"id_table": table.id_table})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        nb_joueurs = res['count']

        print("DAO : Nombre de joueurs assis à une TableJeu - Terminé")

        return nb_joueurs

    def lister(self, joueur=None, seance=None, personnage=None, mj=None) -> list[TableJeu]:
        '''Retourne la liste des tables
        Si les paramètres sont à None, liste toutes les tables
        Params
        ------
        joueur : Joueur
            sélectionne uniquement les tables du joueur
            si None, sélectionne tous les joueurs
        seance : int
            sélectionne uniquement les tables de la séance
            si None, sélectionne toutes les seances
        mj : MaitreJeu
            sélectionne uniquement les tables du mj
            si None, sélectionne tous les mj

        '''

        print("DAO : Lister toutes les tables")

        variables = dict()
        requete = "SELECT t.id_seance,                                             "\
            "             t.id_table,                                              "\
            "             t.scenario,                                              "\
            "             mj.id_joueur AS id_mj,                                   "\
            "             j.pseudo,                                                "\
            "             p.id_personnage                                          "\
            "        FROM jdr.table_jeu t                                          "\
            "        LEFT JOIN jdr.table_personnage tp USING(id_table)             "\
            "        LEFT JOIN jdr.personnage p USING(id_personnage)               "\
            "        LEFT JOIN jdr.joueur j USING (id_joueur)                      "\
            "        LEFT JOIN jdr.joueur mj ON t.id_maitre_jeu = mj.id_joueur     "\
            "       WHERE 1=1                                                      "

        if personnage:
            requete += " AND p.id_personnage = %(id_personnage)s                   "
            variables["id_personnage"] = personnage.id_personnage

        if joueur:
            requete += " AND j.id_joueur = %(id_joueur)s                           "
            variables["id_joueur"] = joueur.id_joueur

        if seance:
            requete += " AND t.id_seance = %(id_seance)s                           "
            variables["id_seance"] = seance

        if mj:
            requete += " AND t.id_maitre_jeu = %(id_mj)s                           "
            variables["id_mj"] = mj.id_joueur

        requete += "ORDER BY t.id_seance, t.id_table;                              "

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(requete, variables)
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        id_table_actuel = None
        id_sceance_actuel = None
        table_jeu = None
        liste_tables_jeu = []

        if res:
            for row in res:
                # Si c est une nouvelle table
                if (row["id_table"] != id_table_actuel or row["id_seance"] != id_sceance_actuel):
                    id_table_actuel = row["id_table"]
                    id_sceance_actuel = row["id_seance"]

                    # On ajoute la table precedente a la liste
                    if table_jeu:
                        liste_tables_jeu.append(table_jeu)

                    maitre_jeu = JoueurDao().trouver_par_id(row["id_mj"])

                    table_jeu = TableJeu(id_table=row["id_table"],
                                         id_seance=row["id_seance"],
                                         maitre_jeu=maitre_jeu,
                                         scenario=row["scenario"],
                                         personnages=[])

                if row["id_personnage"]:
                    table_jeu.personnages.append(
                        PersonnageDao().trouver_par_id(row["id_personnage"]))

            # Ajout a la liste de la derniere table
            liste_tables_jeu.append(table_jeu)

        print("DAO : Lister toutes les tables - Terminé")

        return liste_tables_jeu

    def compter_tables_par_seance(self, seance) -> int:
        print("DAO : Compter Tables")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT count(*)                        "
                        "  FROM jdr.table_jeu                   "
                        " WHERE id_seance = %(id_seance)s       ",
                        {"id_seance": seance})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        nb_tables_par_seance = res['count']

        print("DAO : Compter Tables-terminé")

        return nb_tables_par_seance

    def lister_tables_actives(self) -> list[TableJeu]:
        '''Retourne la liste des tables de jeu avec un Maitre du Jeu et/ou des joueurs
        '''

        print("DAO : Lister tables actives")

        variables = dict()
        requete = "SELECT t.*                                                      "\
            "        FROM jdr.table_jeu t                                          "\
            "       INNER JOIN jdr.table_personnage tp USING(id_table)             "\
            "      UNION                                                           "\
            "      SELECT t.*                                                      "\
            "        FROM jdr.table_jeu t                                          "\
            "       WHERE id_maitre_jeu IS NOT NULL                                "

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(requete, variables)
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        id_table_actuel = None
        id_sceance_actuel = None
        table_jeu = None
        liste_tables_jeu = []

        if res:
            for row in res:
                maitre_jeu = JoueurDao().trouver_par_id(row["id_maitre_jeu"])
                table_jeu = TableJeu(id_table=row["id_table"],
                                     id_seance=row["id_seance"],
                                     maitre_jeu=maitre_jeu,
                                     scenario=row["scenario"])
                table_jeu.personnages = self.lister_personnages(table_jeu)

                liste_tables_jeu.append(table_jeu)

        print("DAO : Lister tables actives - Terminé")

        return liste_tables_jeu

    def gerer_par_mj(self, table, maitre_jeu) -> bool:
        ''' gerer une table pour mj
        '''
        print("DAO : Gerer une table pour mj")

        # if not info_comp:
        #    info_comp = 'null'

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE jdr.table_jeu                           "
                        "   SET id_maitre_jeu = %(id_mj)s,              "
                        "       scenario = %(scenario)s,                "
                        "       infos_complementaires = %(info_comp)s   "
                        " WHERE id_table = %(id_table)s                 "
                        "   AND id_seance = %(id_seance)s               ",
                        {"id_table": table.id_table, "id_seance": table.id_seance,
                         "id_mj": maitre_jeu.id_joueur, "scenario": table.scenario,
                         "info_comp": table.infos_complementaires})
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        print("DAO : Gerer une table pour mj - Terminé")

        return (res == 1)

    def joueurs_assis(self, table) -> list[Joueur]:
        '''Liste des joueurs assis actuellement à la table
        '''
        print("DAO : Liste des joueurs assis à une TableJeu")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT j.*                                        "
                        "  FROM jdr.table_personnage                       "
                        "  JOIN jdr.personnage p USING (id_personnage)     "
                        "  JOIN jdr.joueur j USING (id_joueur)             "
                        " WHERE id_table = %(id_table)s                    ",
                        {"id_table": table.id_table})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        joueur_list = []
        if res:
            for row in res:
                joueur = Joueur(pseudo=row["pseudo"],
                                nom=row["nom"],
                                prenom=row["prenom"],
                                mail=row["mail"],
                                id_joueur=row["id_joueur"])
                joueur_list.append(joueur)

        print("DAO : Liste des joueurs assis à une TableJeu - Terminé")

        return joueur_list

    def tables_sans_maitre_du_jeu(self, seance) -> list[TableJeu]:
        '''Retourne la liste des Tables sans Maître du Jeu de la Séance

        Parameters
        ----------
        seance : Seance

        Returns
        -------
        list[TableJeu] : la liste des Tables sans Maître du Jeu de la Séance
        '''
        print("DAO : Tables sans Maître du Jeu de la Séance")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                                     "
                        "  FROM jdr.table_jeu                                         "
                        " WHERE id_maitre_jeu IS NULL                                 "
                        "   AND id_seance = %(id_seance)s                             ",
                        {"id_seance": seance.id_seance})
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        table_list = []
        if res:
            for row in res:
                table_jeu = TableJeu(id_table=row["id_table"],
                                     id_seance=row["id_seance"])
                table_list.append(table_jeu)

        print("DAO : Tables sans Maître du Jeu de la Séance - Terminé")
        return table_list

    def trouver_mj(self, table) -> int:
        '''Trouver le Maitre du Jeu d'une Table

        Params
        ------
        * table : tableJeu
            * la table sur laquelle on souhaite connaitre le MJ

        Returns
        -------
        L'identifiant du Maître du Jeu ou None s'il n'y a pas de Maître du Jeu à la Table
        '''
        print("DAO : Trouver Maitre du Jeu de la Table")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_maitre_jeu                                         "
                        "  FROM jdr.table_jeu                                         "
                        " WHERE id_table = %(id_table)s                               ",
                        {"id_table": table.id_table})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        id_maitre_jeu = res["id_maitre_jeu"] if res else None

        print("DAO : Trouver Maitre du Jeu de la Table - Terminé")
        return id_maitre_jeu
