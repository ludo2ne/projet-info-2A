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


class TableJeuDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de service de Joueur
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
            table.id = res['id_table']
            created = True

        print("DAO : Création d'une TableJeu - Terminé")

        return created

    def trouver_par_id(self, id_table) -> int:
        '''Obtenir une table à partir de son id_table
        '''

        print("DAO : Trouver TableJeu par id")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM jdr.table WHERE id_table = "
                        "%(id_table)s;", {"id_table": id_table})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        table = None
        if res:

            # TODO trouver mj

            table = TableJeu(id_table=res['id_table'],
                             numero=res['numero'],
                             scenario=res['scenario'])

            table.liste_personnages = lister_personnages(table)

        print("DAO : Trouver TableJeu par id - Terminé")

        return table

    def lister_personnages(self, table):
        '''retourne la liste des personnages de la table
        '''
        # TODO
        return null

    def nombre_joueurs_assis(self, table) -> int:
        '''Nombre de joueurs assis actuellement à la table
        '''
        print("DAO : Nombre de joueurs assis à une TableJeu")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT count(1) FROM jdr.table_personnage WHERE id_table = "
                        "%(id_table)s;", {"id_table": table.id_table})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        nb_joueurs = res['count']

        print("DAO : Nombre de joueurs assis à une TableJeu - Terminé")

        return nb_joueurs

    def lister_toutes(self):
        '''Retourne la liste des tables
                le maitre du jeu,
                le scénario,
                les personnages, 
                les joueurs assis
        '''

        print("DAO : Lister toutes les tables")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT t.id_seance,                                             "
                                   "       t.id_table,                                              "
                                   "       t.scenario,                                              "
                                   "       mj.id_joueur AS id_mj,                                   "
                                   "       j.pseudo,                                                "
                                   "       p.id_personnage                                          "
                                   "  FROM jdr.table_jeu t                                          "
                                   "  LEFT JOIN jdr.table_personnage tp USING(id_table)             "
                                   "  LEFT JOIN jdr.personnage p USING(id_personnage)               "
                                   "  LEFT JOIN jdr.joueur j USING (id_joueur)                      "
                                   "  LEFT JOIN jdr.joueur mj ON t.id_maitre_jeu = mj.id_joueur     "
                                   "  ORDER BY t.id_seance, t.id_table;                             "
                                   )
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        print(res)

        id_table_actuel = None
        id_sceance_actuel = None
        table_jeu = None
        liste_tables_jeu = []

        if res:
            for row in res:
                if (row["id_table"] != id_table_actuel or row["id_seance"] != id_sceance_actuel):
                    id_table_actuel = row["id_table"]
                    id_sceance_actuel = row["id_seance"]
                    if table_jeu:
                        liste_tables_jeu.append(table_jeu)

                    maitre_jeu = JoueurDao().trouver_par_id(row["id_mj"])
                    print("mj trouvé")

                    table_jeu = TableJeu(id_table=row["id_table"],
                                         id_seance=row["id_seance"],
                                         maitre_jeu=maitre_jeu,
                                         scenario=row["scenario"])

                    print("table créée")

                if row["id_personnage"]:
                    table_jeu.personnages.append(
                        PersonnageDao().trouver_par_id(row["id_personnage"]))

        print("DAO : Lister toutes les tables - Terminé")

        return liste_tables_jeu
