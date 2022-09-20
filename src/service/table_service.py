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
        table_dao = TableDao()

        nouvelle_table = Table(numero)
        table_dao.creer(nouvelle_table)

    def ajouter_joueur(self, table, joueur) -> bool:
        '''Service d'ajout d'un joueur à une table'

        Parameters
        ----------
        table : Table
            la table sur laquelle on ajoute le joueur
        joueur : Joueur
            Joueur à ajouter
        '''
        table_dao = TableDao()
        success = False

        nombre_actuel_joueurs = table_dao.get_nb_joueurs(table)

        if nombre_actuel_joueurs <= table.nb_joueurs_max:
            success = table_dao.ajouter_joueur(table, joueur)
        else:
            print("Impossible d'ajouter de nouveaux joueurs à la table")
            print("Nombre de joueurs maximum : " + table.nb_joueurs_max)
            print("Nombre de joueurs actuellement : " + nombre_actuel_joueurs)

        return success
