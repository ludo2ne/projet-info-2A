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

    def creer_table(self, id_seance):
        '''Service de création d'une table
        '''
        print("Service : Création de la TableJeu")
        table = TableJeu(id_table=None, id_seance=id_seance)
        TableJeuDao().creer(table)
        print("Service : Création de la TableJeu - Terminé")
        return table

    def lister(self, joueur=None, seance=None) -> list[TableJeu]:
        '''Retourne la liste des tables
        Si les paramètres sont à None, liste toutes les tables
        Params
        ------
        joueur : Joueur
            sélectionne uniquement les tables du joueur
            si None, sélectionne tous les joueurs
        seance : int
            sélectionne uniquement les tables de la séance
            si None, sélectionne toutes les seances
        '''

        print("Service : Lister toutes les tables")

        liste_tables_jeu = TableJeuDao().lister(joueur, seance)

        print("Service : Lister toutes les tables - Terminé")

        return liste_tables_jeu
