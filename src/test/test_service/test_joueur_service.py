import unittest
import time

from service.joueur_service import JoueurService


class TestJoueurService(unittest.TestCase):

    def test_creer_joueur(self):
        # GIVEN
        pseudo, nom, prenom, mail = "ella" + \
            time.strftime("%M%S"), "Danloss", "Ella", "ella.danloss@wanadoo.fr"

        # WHEN
        nouveau_joueur = JoueurService().creer(pseudo, nom, prenom, mail)

        # THEN
        self.assertEqual("Danloss", nouveau_joueur.nom)
        self.assertEqual("Ella", nouveau_joueur.prenom)
        self.assertEqual("ella.danloss@wanadoo.fr", nouveau_joueur.mail)


if __name__ == '__main__':
    unittest.main()
