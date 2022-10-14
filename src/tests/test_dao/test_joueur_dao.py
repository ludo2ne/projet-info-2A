import time
import unittest

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from dao.table_jeu_dao import TableJeuDao


class TestJoueurDao(unittest.TestCase):
    def test_creer_joueur_ok(self):
        # GIVEN
        joueur_dao = JoueurDao()
        joueur = Joueur(pseudo="Al"+time.strftime("%M%S"),
                        nom="Terrieur",
                        prenom="Alain",
                        mail="alain.terrieur@mail.fr")

        # WHEN
        created = joueur_dao.creer(joueur)

        # THEN
        self.assertTrue(created)
        self.assertIsNotNone(joueur.id)

    def rejoindre_table_ok(self):
        pass
        # TODO
        '''
        # GIVEN
        joueur_dao = JoueurDao()
        table = TableDao().trouver_par_id(2)
        personnage = Personnage()

        # WHEN
        inserted = joueur_dao.rejoindre_table(table, joueur, personnage)

        # THEN
        self.assertTrue(inserted)
        '''


if __name__ == '__main__':
    unittest.main()
