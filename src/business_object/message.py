'''
Module message
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 26/10/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.joueur import Joueur
import time


class Message:
    '''Attributes
    ----------
    id_message : int
        Identifiant unique du message
    id_joueur : int
        Identifiant unique du joueur
    date_creation : time
        Date et heure de la création du message
    contenu : str
        Contenu du message
    lu : boolean
        si le joueur a lu le message


    '''

    def __init__(self, id_message, id_joueur, contenu, lu=False, date_creation=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
        '''Constructeur de l'objet Message
        '''
        print("Objet : Création d'un message")
        self.date_creation = date_creation
        self.id_message = id_message
        self.id_joueur = id_joueur
        self.contenu = contenu
        self.lu = lu

    def as_list(self) -> list[str]:
        '''Permet d'obtenir les informations d'un message

        Parameters
        ----------
        None

        Returns
        -------
        liste : list[str]
            liste des informations du message
        '''
        liste = [self.id_message, self.id_joueur,
                 self.contenu, self.lu, self.date_creation]
        return liste
