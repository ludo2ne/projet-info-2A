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

    def __init__(self, pseudo, nom, prenom, mail, id_joueur=None, liste_personnage=[]):
        '''Constructeur de l'objet
        '''
        print("Objet : Création du joueur : " + pseudo)
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.liste_personnage = liste_personnage
