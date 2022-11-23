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
        # La première séance a pour id 1000, c'est là qu'on va créer la table
        id_seance = 1000
        # On peut lister les tables de la séance avant création de table
        liste_table = TableJeuService().lister(seance=id_seance)
        liste_id_table = [t.id_table for t in liste_table]
        liste_id_table.sort()

        # WHEN
        # On appelle le service de création de table
        nouvelle_table = TableJeuService().creer(id_seance)

        # THEN
        # vérification que la table a été instanciée en même temps qu'elle a été
        # ajoutée dans la BDD (utile pour les tests suivants)
        self.assertIsNotNone(nouvelle_table)

        # On peut vérifier qu'on peut bien la trouver dans la base de données
        self.assertTrue(TableJeuService().trouver_par_id(
            nouvelle_table.id_table) is not None)

        # vérification de l'égalité des valeurs de id_seance
        self.assertEqual(nouvelle_table.id_seance, id_seance)

        # Vérification que cette table n'était pas dans la liste de départ
        self.assertFalse(nouvelle_table.id_table in liste_id_table)

        # Supprimer la table créée afin de ne pas interférer avec les autres tests (lister)
        statut = TableJeuService().supprimer(nouvelle_table)
        if not statut:
            print("Attention cette table n'a pas été supprimée!")

    def test_supprimer(self):
        # GIVEN
        # Nous allons supprimer la table 1003 de la séance 1000
        id_seance = 1000
        id_table = 1003
        # La méthode de suppression demande comme entrée une instanciation de la table
        table_jeu = TableJeu(id_table, id_seance)

        # WHEN
        statut = TableJeuService().supprimer(table_jeu)

        # THEN
        # vérification de la suppression de la table_jeu
        self.assertTrue(statut)
        # On peut vérifier qu'on ne peut pas la trouver dans la base de données
        self.assertTrue(TableJeuService().trouver_par_id(id_table) is None)
        # Alors qu'on trouve bien la table 1000
        self.assertTrue(TableJeuService().trouver_par_id(1000) is not None)

    def test_trouver_par_id(self):
        # GIVEN
        # Nous allons chercher deux tables: la 1000, qui existe dans la BDD et la 1099, qui n'existe pas
        # Voici les caractéristiques attendues de la table 1000
        id_table = 1000
        id_seance = 1000
        joueur = JoueurService().trouver_par_pseudo("mlkjhg")
        mj = MaitreJeu(joueur)
        maitre_jeu = mj
        scenario = "Epidémie au Lazaret"
        infos_complementaires = 'joueurs de niveau 5 minimum'

        # WHEN
        t2 = TableJeuService().trouver_par_id(id_table)
        t3 = TableJeuService().trouver_par_id(1099)

        # THEN
        # vérification que la table trouvée pour 1000 a les caractéristiques attendues
        self.assertEqual(id_table, t2.id_table)
        self.assertEqual(id_seance, t2.id_seance)
        self.assertEqual(maitre_jeu.id_joueur, t2.maitre_jeu.id_joueur)
        self.assertEqual(scenario, t2.scenario)
        self.assertEqual(infos_complementaires, t2.infos_complementaires)
        # vérification qu'aucune table 1099 n'a été trouvée
        self.assertIsNone(t3)

    def test_lister_personnages(self):

        # GIVEN
        # La table 1000 contient 5 personnages dans la BDD (id 1003, 1004, 1005, 1006, 1007),
        # dont les deux définis ci_dessous
        table_jeu = TableJeu(id_table=1000, id_seance=1000)
        perso1 = Personnage(id_personnage=1003, nom="Panoramix",
                            classe="Druid", race="Human", niveau=0)
        perso2 = Personnage(id_personnage=1005, nom="Gimli",
                            classe="Fighter", race="Dwarf", niveau=1)

        # WHEN
        liste_personnages = TableJeuService().lister_personnages(table_jeu)
        liste_perso_as_list = [p.as_list() for p in liste_personnages]
        # Trions les personnages par identifiant croissant.
        liste_perso_as_list.sort(key=lambda perso: perso[0])

        # THEN
        # Vérifions d'abord qu'on a bien 5 personnages dans la liste
        self.assertEqual(len(liste_personnages), 5)
        # Le premier de la liste devrait être perso 1
        self.assertEqual(liste_perso_as_list[0][0], perso1.id_personnage)
        self.assertEqual(liste_perso_as_list[0][1], perso1.nom)
        self.assertEqual(liste_perso_as_list[0][2], perso1.classe)
        self.assertEqual(liste_perso_as_list[0][3], perso1.race)
        self.assertEqual(liste_perso_as_list[0][4], perso1.niveau)
        # Le troisième de la liste devrait être perso2
        self.assertEqual(liste_perso_as_list[2][0], perso2.id_personnage)
        self.assertEqual(liste_perso_as_list[2][1], perso2.nom)
        self.assertEqual(liste_perso_as_list[2][2], perso2.classe)
        self.assertEqual(liste_perso_as_list[2][3], perso2.race)
        self.assertEqual(liste_perso_as_list[2][4], perso2.niveau)

    def test_lister_tables_vides(self):
        # GIVEN
        # Il y a deux tables vides dans la BDD avec un identifiant supérieur à 1000
        nb_table_vide = 2
        liste_id_tables_vides_test = [1002, 1003]

        # WHEN
        # On interroge la BDD pour obtenir toutes les tables vides
        liste_table_vide = TableJeuService().lister_tables_vides()
        # On récupère leurs id et on ne garde que ceux supérieurs à 1000
        liste_id_tables_vides_recuperees = [
            t.id_table for t in liste_table_vide if t.id_table >= 1000]
        # On les trie par ordre croissant pour faciliter la comparaison
        liste_id_tables_vides_recuperees.sort()

        # THEN
        # Comparons la liste obtenue avec celle attendue
        self.assertEqual(liste_id_tables_vides_test,
                         liste_id_tables_vides_recuperees)

    def test_lister(self):
        # La méthode lister prend 3 paramètres optionnels, nous allons tester les différentes combinaisons
        # GIVEN
        pseudo1 = "apzoei"
        pseudo2 = "qmsldk"
        # on utilise des joueurs inscrits dans notre base de données pour faire le test
        joueur1 = JoueurService().trouver_par_pseudo(pseudo1)
        joueur2 = JoueurService().trouver_par_pseudo(pseudo2)
        seance1 = 1000
        seance2 = 1001
        # Test 1: aucun paramètre, on doit obtenir toutes les tables test (id > 1000)
        liste_table1_test = [1000, 1001, 1002, 1003, 1004]
        # Test 2: un paramètre joueur: toutes les tables de joueur 1
        liste_table2_test = [1000, 1004]
        # Test 3: un paramètre séance: toutes les tables de la séance 1000
        liste_table3_test = [1000, 1001, 1002, 1003]
        # Test 4: un paramère complète: toutes les tables complètes
        liste_table4_test = [1000]
        # Test 5: deux paramètres joueur2 et séance2: toutes les tables du joueur2 dans la séance2
        liste_table5_test = [1004]
        # Test 6: deux paramètres joueur1 et complète: toutes les tables complètes du joueur1
        liste_table6_test = [1000]
        # Test 7: deux paramètres séance1 et complète False: toutes les tables incomplètes de la séance 1
        liste_table7_test = [1001, 1002, 1003]
        # Test 8: trois paramètres: toutes les tables complètes de la séance2 avec le joueur2
        liste_table8_test = []

        complete = True

        # WHEN
        # Test 1
        liste_table1 = TableJeuService().lister()
        liste_id_table1 = [
            t.id_table for t in liste_table1 if t.id_table >= 1000]
        liste_id_table1.sort()

        # Test 2
        liste_table2 = TableJeuService().lister(joueur=joueur1)
        liste_id_table2 = [t.id_table for t in liste_table2]
        liste_id_table2.sort()

        # Test 3
        liste_table3 = TableJeuService().lister(seance=seance1)
        liste_id_table3 = [t.id_table for t in liste_table3]
        liste_id_table3.sort()

        # Test 4
        liste_table4 = TableJeuService().lister(complete=complete)
        liste_id_table4 = [t.id_table for t in liste_table4]
        liste_id_table4.sort()

        # Test 5
        liste_table5 = TableJeuService().lister(joueur=joueur2, seance=seance2)
        liste_id_table5 = [t.id_table for t in liste_table5]
        liste_id_table5.sort()

        # Test 6
        liste_table6 = TableJeuService().lister(joueur=joueur1, complete=complete)
        liste_id_table6 = [t.id_table for t in liste_table6]
        liste_id_table6.sort()

        # Test 7
        liste_table7 = TableJeuService().lister(seance=seance1, complete=not complete)
        liste_id_table7 = [t.id_table for t in liste_table7]
        liste_id_table7.sort()

        # Test 8
        liste_table8 = TableJeuService().lister(
            joueur=joueur2, seance=seance2, complete=complete)
        liste_id_table8 = [t.id_table for t in liste_table8]

        # THEN
        # valeur pour la comparaison a verifier
        self.assertEqual(liste_id_table1, liste_table1_test)
        self.assertEqual(liste_id_table2, liste_table2_test)
        self.assertEqual(liste_id_table3, liste_table3_test)
        self.assertEqual(liste_id_table4, liste_table4_test)
        self.assertEqual(liste_id_table5, liste_table5_test)
        self.assertEqual(liste_id_table6, liste_table6_test)
        self.assertEqual(liste_id_table7, liste_table7_test)
        self.assertEqual(liste_id_table8, liste_table8_test)

    def test_est_disponible(self):
        # GIVEN
        # Une table est disponible si elle a moins de 5 joueurs inscrits
        # Table vide donc disponible
        table_jeu1 = TableJeu(id_table=1001, id_seance=1000)
        table_jeu2 = TableJeu(id_table=1000, id_seance=1000)  # Table complète
        # Table avec 2 joueurs donc disponible
        table_jeu3 = TableJeu(id_table=1004, id_seance=1001)

        # WHEN
        dispo1 = TableJeuService().est_disponible(table_jeu1)
        dispo2 = TableJeuService().est_disponible(table_jeu2)
        dispo3 = TableJeuService().est_disponible(table_jeu3)

        # THEN
        self.assertTrue(dispo1)  # Table sans joueur
        self.assertFalse(dispo2)  # Table complète à 5 joueurs
        self.assertTrue(dispo3)  # Table à 2 joueurs

    """def test_affichage_liste(self):          La sortie est un tableau à afficher, comment tester ça?"""

    def test_trouver_mj(self):
        # GIVEN
        joueur1 = JoueurService().trouver_par_pseudo("mlkjhg")
        mj1 = MaitreJeu(joueur1)
        joueur2 = JoueurService().trouver_par_pseudo("qpsodd")
        mj2 = MaitreJeu(joueur2)
        id_table1 = 1000  # Cette table a mj1 pour mj
        id_table2 = 1004  # Cette table a mj2 pour mj
        id_table3 = 1002  # Cette table n'a pas de mj
        table_jeu1 = TableJeuService().trouver_par_id(id_table1)
        table_jeu2 = TableJeuService().trouver_par_id(id_table2)
        table_jeu3 = TableJeuService().trouver_par_id(id_table3)

        # WHEN
        mj1r = TableJeuService().trouver_mj(table_jeu1)
        mj2r = TableJeuService().trouver_mj(table_jeu2)
        mj3r = TableJeuService().trouver_mj(table_jeu3)

        # THEN
        # valeur pour la comparaison a verifier
        self.assertEqual(mj1r.id_joueur, mj1.id_joueur)
        self.assertEqual(mj2r.id_joueur, mj2.id_joueur)
        self.assertIsNone(mj3r)

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
