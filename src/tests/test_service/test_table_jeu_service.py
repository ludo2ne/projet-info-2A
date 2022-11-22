'''
Module test_table_jeu_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


import unittest
import time
import os

from unittest import mock

from service.table_jeu_service import TableJeuService

from dao.db_connection import DBConnection

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage
from business_object.maitre_jeu import MaitreJeu

from business_object.joueur import Joueur


@mock.patch.dict(os.environ, {"NB_JOUEURS_MAX_PAR_TABLE": "5"})
class TestTableJeuService(unittest.TestCase):

    '''Chargement de données spécifiques pour les tests en BDD'''
    @classmethod
    def setUpClass(self):

        test_db = open("data/test_db.sql", encoding="utf-8")
        test_db_as_string = test_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(test_db_as_string)
        except Exception as e:
            print(e)
            raise

    def test_creer(self):
        # GIVEN
        # creer une table en avance avec les personnages pour le test ?
        id_seance = 1
        id_table = 1000

        # WHEN
        nouvelle_table = TableJeuService().creer(id_seance)

        # THEN
        # vérification de l'existance de la table qui vient d'être crée
        self.assertIsNotNone(nouvelle_table)
        # vérification de l'égalité des valeurs de id_seance
        self.assertEqual(nouvelle_table.id_seance, id_seance)

    def test_supprimer(self):
        # GIVEN
        id_seance = 1
        id_table = 1000
        table_jeu = TableJeu(id_table, id_seance)

        # WHEN
        statut = TableJeuService().supprimer(table_jeu)

        # THEN
        # vérification de la suppression de la table_jeu
        self.assertTrue(statut)

    def test_trouver_par_id(self):
        # GIVEN
        t1 = TableJeu(id_table=1000, id_seance=1)

        # WHEN
        t2 = TableJeuService().trouver_par_id(t1.id_table)

        # THEN
        # vérification de ces 2 tables référence un même objet table
        self.assertEqual(t1.id_table, t2.id_table)

    def test_lister_personnages(self):

        # GIVEN
        table_jeu = TableJeu(id_table=1000, id_seance=1)

        # WHEN
        liste_personnages = TableJeuService().lister_personnages(table_jeu)

        # THEN
        # a modifier ? si l'on peut verifier le contenu de la liste de personnage ?
        self.assertEqual(len(liste_personnages), 2)

    def test_lister_tables_vides(self):
        # GIVEN
        nb_table_vide = 5

        # WHEN
        liste_table_vide = TableJeuService().lister_tables_vides()

        # THEN
        self.assertEqual(len(liste_table_vide), nb_table_vide)

    def test_lister(self):
        # GIVEN
        pseudo = "toto"
        # on utilise un joueur est inscrit dans notre base de données pour faire le test
        joueur = JoueurService().trouver_par_pseudo(pseudo)
        seance = 1
        complete = True

        # WHEN
        liste_table1 = TableJeuService().lister(joueur)
        liste_table2 = TableJeuService().lister(seance)
        liste_table3 = TableJeuServie().lister(joueur, seance, complete)
        liste_table4 = TableJeuService().lister(joueur, seance)

        # THEN
        # valeur pour la comparaison a verifier
        self.assertEqual(len(liste_table1), 2)
        self.assertEqual(len(liste_table2), 3)
        self.assertEqual(len(liste_table3), 5)  # idée : erreur ici
        self.assertEqual(len(liste_table4), 2)

    def test_est_disponible(self):
        # GIVEN
        table_jeu1 = TableJeu(id_table=2, id_seance=1)
        table_jeu2 = TableJeu(id_table=1000, id_seance=1)

        # WHEN
        dispo1 = TableJeuService().est_disponible(table_jeu1)
        dispo2 = TableJeuService().est_disponible(table_jeu2)

        # THEN
        self.assertEqual(dispo1, True)  # valeur pour la comparaison a verifier
        self.assertEqual(dispo2, False)  # idée : erreur ici

    """def test_affichage_liste(self):          pour l'instant, aucune idée"""

    def test_trouver_mj(self):
        # GIVEN
        mj1 = MaitreJeu("Ahj", "DUPONT", "Alice", "alice.dupont@gmail.com")
        mj2 = MaitreJeu("Bha", "BATON", "Pierre", "pierre.baton@gmail.com")
        table_jeu1 = TableJeu(id_table=2, id_seance=1, maitre_jeu=mj1)
        table_jeu2 = TableJeu(id_table=1000, id_seance=1, maitre_jeu=mj2)

        # WHEN
        mj1r = TableJeuService().est_disponible(table_jeu1)
        mj2r = TableJeuService().est_disponible(table_jeu2)

        # THEN
        self.assertEqual(mj1r, mj1)  # valeur pour la comparaison a verifier
        self.assertEqual(mj2r, mj2)  # idée : erreur ici

    '''Suppression en BDD des données test'''
    @classmethod
    def tearDownClass(self):

        test_db_drop = open("data/test_db_drop.sql", encoding="utf-8")
        test_db_drop_as_string = test_db_drop.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(test_db_drop_as_string)
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    unittest.main()
