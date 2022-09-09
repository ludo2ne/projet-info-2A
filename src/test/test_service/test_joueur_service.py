import unittest

from service.joueur_service import JoueurService


class TestJoueurService(unittest.TestCase):
    ''' Test de la classe ImporterCSV 
        Classe de la couche service
    '''

    def test_creer_joueur(self):
        # GIVEN
        nom, prenom = "Javel", "Aude"

        # WHEN
        nouveau_joueur = JoueurService().creer_joueur(nom, prenom)

        # THEN
        self.assertEqual("Javel", nouveau_joueur.nom)
        self.assertEqual("Aude", nouveau_joueur.prenom)


if __name__ == '__main__':
    unittest.main()
