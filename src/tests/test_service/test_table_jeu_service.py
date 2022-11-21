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
from unittest.mock import Mock
from unittest.mock import create_autospec

from service.table_jeu_service import TableJeuService

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage


@mock.patch.dict(os.environ, {"NB_JOUEURS_MAX_PAR_TABLE": "5"})
class TestTableJeuService(unittest.TestCase):

    def test_creer_ok(self):
        # GIVEN
        id_seance = 3
        table_jeu = TableJeu(1, id_seance)

        TableJeuDao = Mock()
        TableJeuDao.creer.return_value = table_jeu

        # WHEN
        nouvelle_table = TableJeuService().creer(id_seance)

        # THEN
        self.assertIsNotNone(nouvelle_table)
        self.assertEqual(nouvelle_table.id_seance, 3)

    def test_supprimer(self):
        # GIVEN
        table_jeu = TableJeu(500, 3)

        mock_function = create_autospec(supprimer, return_value=True)

        # WHEN
        statut = TableJeuService().supprimer(table_jeu)

        # THEN
        self.assertTrue(statut)

    def test_trouver_par_id(self):
        # GIVEN
        t1 = TableJeu(id_table=2, id_seance=3)

        TableJeuDao = Mock()
        TableJeuDao.trouver_par_id.return_value = t1

        # WHEN
        t2 = TableJeuService().trouver_par_id(t1.id_table)

        # THEN
        self.assertEqual(t1.id_table, t2.id_table)


#    def test_lister_personnages(self):
#        # GIVEN
#        p1 = Personnage(id_personnage=1, nom="a",
#                        classe="Fighter", race="Human", niveau=1)
#        p2 = Personnage(id_personnage=1, nom="b",
#                        classe="Sorcerer", race="Elf", niveau=1)
#        liste_in = [p1, p2]
#        table_jeu = TableJeu(id_table=500, id_seance=1,
#                             personnages=liste_in)
#
#        TableJeuDao = Mock()
#        TableJeuDao.lister_personnages.return_value = liste_in
#
#        # WHEN
#        liste_out = TableJeuService().lister_personnages(table_jeu)
#
#        # THEN
#        self.assertEqual(len(liste_out), len(liste_in))


if __name__ == '__main__':
    unittest.main()
