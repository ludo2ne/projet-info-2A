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
from service.joueur_service import JoueurService

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
        print("Test de la méthode creer")
        id_seance = 1000
        id_table = 1005

        # WHEN
        nouvelle_table = TableJeuService().creer(id_seance)

        # THEN
        # vérification de l'existance de la table qui vient d'être crée
        self.assertIsNotNone(nouvelle_table)

        # vérification de l'égalité des valeurs de id_seance
        self.assertEqual(nouvelle_table.id_seance, id_seance)

        # Supprimer la table créée afin de ne pas interférer avec les autres tests
        statut = TableJeuService().supprimer(nouvelle_table)
        if not statut:
            print("Attention cette table n'a pas été supprimée!")
        print("Fin de test de la méthode creer")

    def test_supprimer(self):
        # GIVEN
        id_seance = 1000
        id_table = 1003
        table_jeu = TableJeu(id_table, id_seance)

        # WHEN
        statut = TableJeuService().supprimer(table_jeu)

        # THEN
        # vérification de la suppression de la table_jeu
        self.assertTrue(statut)

    def test_trouver_par_id(self):
        # GIVEN
        joueur = JoueurService().trouver_par_pseudo("mlkjhg")
        mj = MaitreJeu(joueur)
        t1 = TableJeu(id_table=1000, id_seance=1000, maitre_jeu=mj, scenario="Epidémie au Lazaret",
                      infos_complementaires='joueurs de niveau 5 minimum')

        # WHEN
        t2 = TableJeuService().trouver_par_id(t1.id_table)

        # THEN
        # vérification que ces 2 tables référencent un même objet table
        self.assertEqual(t1.id_table, t2.id_table)
        self.assertEqual(t1.id_seance, t2.id_seance)
        self.assertEqual(t1.maitre_jeu.id_joueur, t2.maitre_jeu.id_joueur)
        self.assertEqual(t1.scenario, t2.scenario)
        self.assertEqual(t1.infos_complementaires, t2.infos_complementaires)

    def test_lister_personnages(self):

        # GIVEN
        table_jeu = TableJeu(id_table=1000, id_seance=1000)
        perso1 = Personnage(id_personnage=1003, nom="Panoramix",
                            classe="Druid", race="Human", niveau=0)
        perso2 = Personnage(id_personnage=1005, nom="Gimli",
                            classe="Fighter", race="Dwarf", niveau=1)

        # WHEN
        liste_personnages = TableJeuService().lister_personnages(table_jeu)
        liste_perso_as_list = [p.as_list() for p in liste_personnages]
        liste_perso_as_list.sort(key=lambda perso: perso[0])

        # THEN
        # a modifier ? si l'on peut verifier le contenu de la liste de personnage ?
        self.assertEqual(len(liste_personnages), 5)
        self.assertEqual(liste_perso_as_list[0][0], perso1.id_personnage)
        self.assertEqual(liste_perso_as_list[0][1], perso1.nom)
        self.assertEqual(liste_perso_as_list[0][2], perso1.classe)
        self.assertEqual(liste_perso_as_list[0][3], perso1.race)
        self.assertEqual(liste_perso_as_list[0][4], perso1.niveau)
        self.assertEqual(liste_perso_as_list[2][0], perso2.id_personnage)
        self.assertEqual(liste_perso_as_list[2][1], perso2.nom)
        self.assertEqual(liste_perso_as_list[2][2], perso2.classe)
        self.assertEqual(liste_perso_as_list[2][3], perso2.race)
        self.assertEqual(liste_perso_as_list[2][4], perso2.niveau)

    def test_lister_tables_vides(self):
        # GIVEN
        nb_table_vide = 2
        liste_id_tables_vides_test = [1002, 1003]

        # WHEN
        liste_table_vide = TableJeuService().lister_tables_vides()
        liste_id_tables_vides_recuperees = [
            t.id_table for t in liste_table_vide if t.id_table >= 1000]
        liste_id_tables_vides_recuperees.sort()

        # THEN
        self.assertEqual(len(liste_id_tables_vides_recuperees), nb_table_vide)
        self.assertEqual(liste_id_tables_vides_test,
                         liste_id_tables_vides_recuperees)

    def test_lister(self):
        # GIVEN
        pseudo1 = "apzoei"
        pseudo2 = "qmsldk"
        # on utilise un joueur est inscrit dans notre base de données pour faire le test
        joueur1 = JoueurService().trouver_par_pseudo(pseudo1)
        joueur2 = JoueurService().trouver_par_pseudo(pseudo2)
        seance1 = 1000
        seance2 = 1001
        liste_table1_test = [1000, 1004]
        liste_table2_test = [1000, 1001, 1002, 1003]
        liste_table3_test = [1000]
        liste_table4_test = [1000]
        liste_table5_test = []
        complete = True

        # WHEN
        liste_table1 = TableJeuService().lister(joueur=joueur1)
        liste_id_table1 = [t.id_table for t in liste_table1]
        liste_id_table1.sort()

        liste_table2 = TableJeuService().lister(seance=seance1)
        liste_id_table2 = [t.id_table for t in liste_table2]
        liste_id_table2.sort()

        liste_table3 = TableJeuService().lister(
            joueur=joueur1, seance=seance1, complete=complete)
        liste_id_table3 = [t.id_table for t in liste_table3]
        liste_id_table3.sort()

        liste_table4 = TableJeuService().lister(joueur=joueur2, seance=seance1)
        liste_id_table4 = [t.id_table for t in liste_table4]
        liste_id_table4.sort()

        liste_table5 = TableJeuService().lister(
            joueur=joueur1, seance=seance2, complete=complete)
        liste_id_table5 = [t.id_table for t in liste_table5]

        # THEN
        # valeur pour la comparaison a verifier
        self.assertEqual(liste_id_table1, liste_table1_test)
        self.assertEqual(liste_id_table2, liste_table2_test)
        self.assertEqual(liste_id_table3, liste_table3_test)
        self.assertEqual(liste_id_table4, liste_table4_test)
        self.assertEqual(liste_id_table5, liste_table5_test)

    def test_est_disponible(self):
        # GIVEN
        table_jeu1 = TableJeu(id_table=1001, id_seance=1000)
        table_jeu2 = TableJeu(id_table=1000, id_seance=1000)
        table_jeu3 = TableJeu(id_table=1004, id_seance=1001)

        # WHEN
        dispo1 = TableJeuService().est_disponible(table_jeu1)
        dispo2 = TableJeuService().est_disponible(table_jeu2)
        dispo3 = TableJeuService().est_disponible(table_jeu3)

        # THEN
        self.assertEqual(dispo1, True)  # Table sans joueur
        self.assertEqual(dispo2, False)  # Table complète à 5 joueurs
        self.assertEqual(dispo3, True)  # Table à 1 joueur

    """def test_affichage_liste(self):          La sortie est un tableau à afficher, comment tester ça?"""

    def test_trouver_mj(self):
        # GIVEN
        joueur1 = JoueurService().trouver_par_pseudo("mlkjhg")
        mj1 = MaitreJeu(joueur1)
        joueur2 = JoueurService().trouver_par_pseudo("qpsodd")
        mj2 = MaitreJeu(joueur2)
        id_table1 = 1000
        id_table2 = 1004
        table_jeu1 = TableJeuService().trouver_par_id(id_table1)
        table_jeu2 = TableJeuService().trouver_par_id(id_table2)

        # WHEN
        mj1r = TableJeuService().trouver_mj(table_jeu1)
        mj2r = TableJeuService().trouver_mj(table_jeu2)

        # THEN
        # valeur pour la comparaison a verifier
        self.assertEqual(mj1r.id_joueur, mj1.id_joueur)
        self.assertEqual(mj2r.id_joueur, mj2.id_joueur)  # idée : erreur ici

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
