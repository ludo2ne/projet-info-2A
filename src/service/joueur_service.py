'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao


class JoueurService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer_joueur(self, nom, prenom):
        '''Service de création d'un joueur

        Parameters
        ----------
        nom : str
            nom du joueur
        prenom : str
            prenom du joueur
        '''
        nouveau_joueur = Joueur(nom, prenom)
        JoueurDao.creer(nouveau_joueur)
