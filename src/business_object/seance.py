'''
Module seance
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 26/10/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.joueur import Joueur
import time


class Seance:
    '''Attributes
    ----------
    id_seance : int
        Identifiant unique de la Séance
    description : str
        Description de la Séance
    debut : date
        Début de la Séance
    fin : date
        Fin de la Séance
    '''

    def __init__(self, id_seance, description, debut, fin):
        '''Constructeur de l'objet Séance
        '''
        print("Objet : Création d'une Séance")
        self.id_seance = id_seance
        self.description = description
        self.debut = debut
        self.fin = fin
