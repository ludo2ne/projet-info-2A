'''
Module table
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


class Table:
    '''Attributes
    ----------
    numero : int
        Numéro de la table
    liste_joueurs : list[joueur]
        Liste des joueurs inscrits à la table
    '''

    def __init__(self, numero):
        '''Constructeur de l'objet Table
        '''
        self.liste_joueurs = []
        self.numero = numero
