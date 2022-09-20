import time
import unittest

from business_object.table import Table
from business_object.joueur import Joueur
from dao.table_dao import TableDao


class TestAttackDao(unittest.TestCase):
    def test_create_table_ok(self):
        # GIVEN
        table_dao = TableDao()
        table = Table(numero=12)

        # WHEN
        created = table_dao.creer(table)

        # THEN
        self.assertTrue(created)
        self.assertIsNotNone(table.id)

    def test_ajouter_joueur_ok(self):
        # GIVEN
        table_dao = TableDao()
        table = Table(numero=86)
        table.id = 2
        joueur = Joueur("Danloss", "Ella")
        joueur.id = 4

        # WHEN
        inserted = table_dao.ajouter_joueur(table, joueur)

        # THEN
        self.assertTrue(inserted)

    def test_nombre_joueurs_assis(self):
        # GIVEN
        table_dao = TableDao()
        table = Table(numero=1000)
        table.id = 1000

        # WHEN
        nb_joueurs = table_dao.nombre_joueurs_assis(table)
        print(nb_joueurs)

        # THEN
        self.assertEqual(nb_joueurs, 2)


if __name__ == '__main__':
    unittest.main()
