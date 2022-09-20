import time
import unittest

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao


class TestAttackDao(unittest.TestCase):
    def test_creer_joueur_ok(self):
        # GIVEN
        joueur_dao = JoueurDao()
        joueur = Joueur("Terrieur", "Alain")

        # WHEN
        created = joueur_dao.creer(joueur)

        # THEN
        self.assertTrue(created)
        self.assertIsNotNone(joueur.id)


if __name__ == '__main__':
    unittest.main()
