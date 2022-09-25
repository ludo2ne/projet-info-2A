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
    pseudo : str
        pseudo du joueur
    nom : str
        nom du joueur
    prenom : str
        prenom du joueur
    id : int
        identifiant
    '''

    def __init__(self, pseudo, nom, prenom, mail, id=None):
        '''Constructeur de l'objet
        '''
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.id = id
        self.liste_personnage = []
