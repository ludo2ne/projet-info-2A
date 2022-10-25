import time
import unittest

from business_object.joueur import Joueur
from dao.personnage_dao import PersonnageDao
from dao.table_jeu_dao import TableJeuDao
from service.joueur_service import JoueurService
from utils.reset_database import ResetDatabase


class TestPersonnageDao(unittest.TestCase):
    def test_perso_quitter_table_ok(self):
        # GIVEN
        succes = ResetDatabase().lancer()
        message = "Ré-initilisation de la base de données terminée" if succes else None

        perso_dao = PersonnageDao()
        joueur = JoueurService().trouver_par_pseudo("pp")

        # WHEN
        pb_rencontre = 0
        pb_list_joueur = []
        for el in joueur.liste_personnages:
            perso_utilise = (
                PersonnageDao().lister_tables(el) > 0)
            if perso_utilise:
                perso_enleve_table = PersonnageDao().quitter_table(el)
                if not perso_enleve_table:
                    pb_rencontre += 1
                    pb_list_joueur.append(el.nom)
        if pb_rencontre != 0:
            print("problème rencontré au moment d'enlever ce(s) personnage(s)" +
                  "d'une table:\n" +
                  f"{pb_list_joueur}")

        suppressed = (pb_rencontre == 0)
        tables_utilisees = 0
        for el in joueur.liste_personnages:
            tables_utilisees += PersonnageDao().lister_tables(el)

        # THEN
        self.assertTrue(suppressed)
        self.assertTrue(tables_utilisees == 0)


if __name__ == '__main__':
    unittest.main()
