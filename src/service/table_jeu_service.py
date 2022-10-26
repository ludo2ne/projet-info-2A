'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage

from dao.table_jeu_dao import TableJeuDao


class TableJeuService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer_table(self, id_seance):
        '''Service de création d'une Table de Jeu
        '''
        print("Service : Création de la TableJeu")
        table = TableJeu(id_table=None, id_seance=id_seance)
        TableJeuDao().creer(table)
        print("Service : Création de la TableJeu - Terminé")
        return table

    def lister_personnages(self, id_table) -> list[Personnage]:
        '''Lister les personnages d'une Table de Jeu
        '''
        print("Service : Lister personnages d'une table")
        table_jeu = TableJeuDao().trouver_par_id(id_table)
        liste_personnages = TableJeuDao().lister_personnages(table_jeu)
        print("Service : Lister personnages d'une table - Terminé")
        return liste_personnages
