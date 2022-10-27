'''
Module personnage_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage
from business_object.joueur import Joueur

from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao


class PersonnageService:

    def trouver_par_id(self, id_personnage) -> Personnage:
        '''Trouver un personnage grace à son id
        Params
        ------
        * id_personnage : int
            * id du personnage recherché
        '''
        print("Service : trouver Personnage à partir de son id")
        return PersonnageDao().trouver_par_id(id_personnage)

    def trouver_joueur(self, personnage) -> Joueur:
        '''Trouver le joueur à qui appartient le Personnage
        Params
        ------
        * personnage : Personnage

        Returns
        -------
        * le Joueur propriétaire du Personnage
        '''
        print("Service : trouver Joueur à partir de Personnage")
        return PersonnageDao().trouver_joueur(personnage)

    def rejoindre_table(self, table, personnage):
        '''Ajouter un personnage à une table de jeu

        Parameters
        ----------
        * personnage : Personnage
            * le personnage à ajouter
        * table : TableJeu
            * la table de jeu que le personnage rejoint

        Returns
        -------
        * True si l'opération est un succés
        * False sinon

          '''
        print("Service : Personnage rejoint une table")
        success = PersonnageDao().rejoindre_table(table, personnage)
        print("Service : Personnage rejoint une table - Terminé")
        return success

    def quitter_table(self, table, personnage):
        '''Le personnage quitte une table de jeu

        Parameters
        ----------
        * personnage : Personnage
            * le personnage à ajouter
        * table : TableJeu
            * la table de jeu que le personnage quitte

        Returns
        -------
        * True si l'opération est un succés
        * False sinon
        '''
        print("Service : Personnage quitte une table")
        success = PersonnageDao().quitter_table(table, personnage)
        print("Service : Personnage quitte une table - Terminé")
        return success
