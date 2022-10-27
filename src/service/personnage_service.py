'''
Module personnage_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage

from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao


class PersonnageService:

    def trouver_par_id(self, id_personnage):
        '''Trouver un personnage grace à son id
        Params
        ------
        id_personnage : int
            id du personnage recherché
        '''
        return PersonnageDao().trouver_par_id(id_personnage)

    def rejoindre_table(self, table, personnage):
        '''Ajouter un personnage à une table de jeu

          Parameters
          ----------
          personnage : Personnage
              le personnage à ajouter
          table : TableJeu
              la table de jeu que le personnage rejoint
          '''
        print("Service : Personnage rejoint une table")
        success = PersonnageDao().rejoindre_table(table, personnage)
        print("Service : Personnage rejoint une table - Terminé")
        return success
