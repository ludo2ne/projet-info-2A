import unittest
import time

from business_object.personnage import Personnage


class TestPersonnage(unittest.TestCase):

    def test_creer_personnage(self):
        # GIVEN
        id, nom, classe, race, niveau = 3, "Gandalf", "Magicien", "Humain", 99

        # WHEN
        nouveau_perso = Personnage(
            id, nom, classe, race, niveau)

        # THEN
        self.assertEqual("Gandalf", nouveau_perso.nom)
        self.assertEqual("Magicien", nouveau_perso.classe)
        self.assertEqual("Humain", nouveau_perso.race)
        return nouveau_perso


if __name__ == '__main__':
    a = TestPersonnage().test_creer_personnage()
    print(a.as_list())
