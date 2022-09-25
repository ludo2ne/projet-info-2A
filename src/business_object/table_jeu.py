'''
Module table_jeu
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


class TableJeu:
    '''Attributes
    ----------
    numero : int
        Numéro de la table
    maitre_du_jeu : MaitreJeu
        Le Maitre du Jeu
    personnages : list[Personnage]
        Liste des personnages des joueurs inscrits à la table
    id_table : int
        Identifiant unique de la table de jeu
    nb_joueurs_max : int
        Nombre maximum de joueurs

    '''

    def __init__(self, numero, maitre_jeu=None, personnages=[], id_table=None):
        '''Constructeur de l'objet Table
        '''
        self.numero = numero
        self.maitre_jeu = maitre_jeu
        self.personnages = personnages
        self.nb_joueurs_max = 5
        self.id_table = id_table
