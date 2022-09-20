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
    maitre_du_jeu : MaitreDuJeu
        Le Maitre du Jeu
    liste_joueurs : list[joueur]
        Liste des joueurs inscrits à la table
    nb_joueurs_max : int
        Nombre maximum de joueurs

    '''

    def __init__(self, numero):
        '''Constructeur de l'objet Table

        Parameters
        ----------
        numero : int
            le numéro de la table
        '''
        self.numero = numero
        self.maitre_du_jeu = None
        self.liste_joueurs = []
        self.nb_joueurs_max = 5
