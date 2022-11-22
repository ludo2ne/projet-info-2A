'''
Module test_table_jeu_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


import unittest
import time
import os

from unittest import mock

from service.table_jeu_service import TableJeuService

from dao.db_connection import DBConnection

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage


@mock.patch.dict(os.environ, {"NB_JOUEURS_MAX_PAR_TABLE": "5"})
class TestTableJeuService(unittest.TestCase):

    '''Chargement de données spécifiques pour les tests en BDD'''
    @classmethod
    def setUpClass(self):

        test_db = open("data/test_db.sql", encoding="utf-8")
        test_db_as_string = test_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(test_db_as_string)
        except Exception as e:
            print(e)
            raise

    def test_creer(self):
        # GIVEN
        # creer une table en avance avec les personnages pour le test ?
        id_seance = 1
        id_table = 1000

        # WHEN
        nouvelle_table = TableJeuService().creer(id_seance)

        # THEN
        # vérification de l'existance de la table qui vient d'être crée
        self.assertIsNotNone(nouvelle_table)
        # vérification de l'égalité des valeurs de id_seance
        self.assertEqual(nouvelle_table.id_seance, id_seance)

    def test_supprimer(self):
        # GIVEN
        id_seance = 1
        id_table = 1000
        table_jeu = TableJeu(id_table, id_seance)

        # WHEN
        statut = TableJeuService().supprimer(table_jeu)

        # THEN
        # vérification de la suppression de la table_jeu
        self.assertTrue(statut)

    def test_trouver_par_id(self):
        # GIVEN
        t1 = TableJeu(id_table=1000, id_seance=1)

        # WHEN
        t2 = TableJeuService().trouver_par_id(t1.id_table)

        # THEN
        # vérification de ces 2 tables référence un même objet table
        self.assertEqual(t1.id_table, t2.id_table)

    def test_lister_personnages(self):

        # GIVEN
        table_jeu = TableJeu(id_table=1000, id_seance=1)

        # WHEN
        liste_personnages = TableJeuService().lister_personnages(table_jeu)

        # THEN
        # a modifier ? si l'on peut verifier le contenu de la liste de personnage ?
        self.assertEqual(len(liste_personnages), 2)

    """def test_lister_tables_vides (self) : """

    def test_lister(self):
    '''Suppression en BDD des données test'''
    @classmethod
    def tearDownClass(self):

        test_db_drop = open("data/test_db_drop.sql", encoding="utf-8")
        test_db_drop_as_string = test_db_drop.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(test_db_drop_as_string)
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    unittest.main()
