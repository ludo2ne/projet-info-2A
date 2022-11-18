import unittest
import time

from service.table_jeu_service import TableJeuService


class TestTableJeuService(unittest.TestCase):

    def test_creer(self):
        # GIVEN
        id_seance = 3

        # WHEN
        nouveau_joueur = JoueurService().creer(pseudo, nom, prenom, mail)

        # THEN
        self.assertEqual("Danloss", nouveau_joueur.nom)
        self.assertEqual("Ella", nouveau_joueur.prenom)
        self.assertEqual("ella.danloss@wanadoo.fr", nouveau_joueur.mail)


if __name__ == '__main__':
    unittest.main()
