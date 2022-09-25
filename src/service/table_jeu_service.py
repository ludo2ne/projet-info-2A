'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


from business_object.table_jeu import TableJeu
from dao.table_jeu_dao import TableJeuDao


class TableJeuService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer_table(self, table):
        '''Service de création d'une table
        '''
        table_jeu_dao = TableJeuDao()
        table_dao.creer(table)
