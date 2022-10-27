import time
import unittest

from business_object.joueur import Joueur
from business_object.maitre_jeu import MaitreJeu
from dao.maitre_jeu_dao import MaitreJeuDao
from dao.table_jeu_dao import TableJeuDao
from service.joueur_service import JoueurService
from utils.reset_database import ResetDatabase


class TestMaitreJeuDao(unittest.TestCase):
    def test_mj_quitter_table_ok(self):
        # GIVEN
        succes = ResetDatabase().lancer()
        message = "Ré-initilisation de la base de données terminée" if succes else None

        joueur = JoueurService().trouver_par_pseudo("evabien")

        # WHEN
        listini = []
        listfin = []
        if type(joueur) == MaitreJeu:
            listini = MaitreJeuDao().lister_tables_mj(joueur)
            for el in listini:
                statut = MaitreJeuDao().quitter_table(joueur, el[1])
            listfin = MaitreJeuDao().lister_tables_mj(joueur)
        else:
            statut = False

        # THEN
        self.assertTrue(statut)
        self.assertTrue(len(listfin) == 0 and len(listini) > 0)


if __name__ == '__main__':
    unittest.main()
