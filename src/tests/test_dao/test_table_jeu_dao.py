import time
import unittest

from business_object.table_jeu import TableJeu
from business_object.joueur import Joueur
from dao.table_jeu_dao import TableJeuDao


class TestTableJeuDao(unittest.TestCase):
    def test_create_table_ok(self):
        # GIVEN
        table = TableJeu(id_table=None, id_seance=1)

        # WHEN
        created = TableJeuDao().creer(table)

        # THEN
        self.assertTrue(created)

    def test_nombre_joueurs_assis(self):
        # GIVEN
        table = TableJeu(id_table=1, id_seance=1)

        # WHEN
        nb_joueurs = TableJeuDao().nombre_joueurs_assis(table)
        print("Nombre de joueurs assis : " + str(nb_joueurs))

        # THEN
        self.assertEqual(nb_joueurs, 3)


if __name__ == '__main__':
    unittest.main()
