'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


from business_object.table import Table
from dao.table_dao import TableDao


class TableService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer_table(self, numero):
        '''Service de création d'une table

        Parameters
        ----------
        nom : str
            nom du joueur
        prenom : str
            prenom du joueur
        '''
        nouvelle_table = Table(numero)
        TableDao.creer(nouvelle_table)
