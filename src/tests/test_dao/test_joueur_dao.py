import time
import unittest

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from dao.table_jeu_dao import TableJeuDao
from utils.reset_database import ResetDatabase
from service.joueur_service import JoueurService


class TestJoueurDao(unittest.TestCase):
    def test_creer_joueur_ok(self):
        # GIVEN
        joueur = Joueur(pseudo="Al"+time.strftime("%M%S"),
                        nom="Terrieur",
                        prenom="Alain",
                        mail="alain.terrieur@mail.fr")

        # WHEN
        created = JoueurDao().creer(joueur)

        # THEN
        self.assertTrue(created)
        self.assertIsNotNone(joueur.id)

    def test_lister_tables_ok(self):
        # GIVEN
        succes = ResetDatabase().lancer()
        message = "Ré-initilisation de la base de données terminée" if succes else None

        joueur = JoueurService().trouver_par_pseudo("pp")

        # WHEN
        table_list = JoueurDao().lister_tables(joueur)
        print(table_list)
        # THEN
        self.assertIsNotNone(table_list)

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
