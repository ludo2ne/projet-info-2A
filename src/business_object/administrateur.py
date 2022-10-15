'''
Module administrateur
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


class Administrateur:
    '''Attributes
    -------------
    id_admin : int
        id de l'administrateur
    pseudo : str
        pseudo de l'administrateur
    '''

    def __init__(self, id_admin, pseudo):
        self.id_admin = id_admin
        self.pseudo = pseudo
