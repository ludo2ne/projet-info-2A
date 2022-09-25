import time
import unittest

from business_object.table_jeu import TableJeu
from business_object.joueur import Joueur
from dao.table_jeu_dao import TableJeuDao


class TestTableJeuDao(unittest.TestCase):
    def test_create_table_ok(self):
        # GIVEN
        table_jeu_dao = TableJeuDao()
        table = TableJeu(numero=12)

        # WHEN
        created = table_jeu_dao.creer(table)

        # THEN
        self.assertTrue(created)
        self.assertIsNotNone(table.id)

    def test_nombre_joueurs_assis(self):
        # GIVEN
        table_jeu_dao = TableJeuDao()
        table = TableJeu(numero=1000)
        table.id = 1

        # WHEN
        nb_joueurs = table_jeu_dao.nombre_joueurs_assis(table)
        print("Nombre de joueurs assis : " + str(nb_joueurs))

        # THEN
        self.assertEqual(nb_joueurs, 3)


if __name__ == '__main__':
    unittest.main()
