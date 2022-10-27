'''
Module maitre_jeu
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.joueur import Joueur


class MaitreJeu(Joueur):
    '''Classe MaitreJeu hérite de Joueur

    Attributes
    ----------
    pseudo : str
        pseudo du maître du jeu
    nom : str 
        nom du maître du jeu
    prenom : str
        prenom du maître du jeu 
    mail : str 
        mail du maître du jeu
    id_joueur : int
        id du maître du jeu
    liste_personnages : list[Personnage]
        liste des personnages que le maître du jeu possède lorsqu'il est joueur sur une autre table

    '''

    def __init__(self, pseudo, nom, prenom, mail, id_joueur=None, liste_personnages=[]):
        '''Constructeur de Maître du Jeu à partir d'un joueur
        '''
        super().__init__(pseudo,
                         nom,
                         prenom,
                         mail,
                         id_joueur=None,
                         liste_personnages=[])

    def __init__(self, joueur):
        super().__init__(joueur.pseudo,
                         joueur.nom,
                         joueur.prenom,
                         joueur.mail,
                         joueur.id_joueur,
                         joueur.liste_personnages)
