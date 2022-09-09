'''
Module joueur
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


class Joueur:
    '''Attributes
    ----------
    nom : str
        nom du joueur
    prenom : str
        prenom du joueur
    id : int
        identifiant
    '''

    def __init__(self, nom, prenom):
        '''Constructeur de l'objet
        L'id est généré automatiquement lors de l'insert en bdd'

        Parameters
        ----------
        nom : str
            nom du joueur
        prenom : str
            prenom du joueur
        '''
        self.nom = nom
        self.prenom = prenom
