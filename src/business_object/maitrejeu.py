'''
Module maitre_jeu
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from src.business_object.joueur import Joueur


class MaitreJeu(Joueur):
    '''Classe MaitreJeu hérite de Joueur
    '''

    def __init__(self, pseudo, nom, prenom, mail, id_joueur=None, liste_personnages=[]):
        super().__init__(pseudo, nom, prenom, mail, id_joueur=None, liste_personnages=[])
