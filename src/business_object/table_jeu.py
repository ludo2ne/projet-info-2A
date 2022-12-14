'''
Module table_jeu
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

import os

from business_object.maitre_jeu import MaitreJeu
from business_object.personnage import Personnage


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

    def __init__(self, id_table, id_seance, maitre_jeu=None, scenario=None, infos_complementaires=None, personnages=[]):
        '''Constructeur de l'objet Table

        Parameters
        ----------
        id_table : int
            numéro de la table
        id_seance : int
            numéro de la séance
        maitre_jeu : MaitreJeu
            maître du jeu de la table
        scenario : str
            sénario choisi par le maître du jeu
        infos_complementaires : str
            informations complémentaires
        personnages : list[Personnage]
            liste des personnages présents sur la table
        '''
        print("Objet : Création d'une TableJeu")
        self.id_table = id_table
        self.id_seance = id_seance
        self.maitre_jeu = maitre_jeu
        self.scenario = scenario
        self.infos_complementaires = infos_complementaires
        self.personnages = personnages
        self.nb_joueurs_max = int(os.environ["NB_JOUEURS_MAX_PAR_TABLE"])

    def as_list(self):
        '''Renvoie les information de la table

        Parameters
        ----------
        None

        Returns
        -------
        liste : list[str]
            information de la table sous forme de liste
        '''
        mj_pseudo = self.maitre_jeu.pseudo if self.maitre_jeu else ""
        liste = [self.id_seance, self.id_table,
                 self.scenario, mj_pseudo]
        return liste

    def liste_perso(self) -> list[Personnage]:
        '''Renvoie liste des personnages présent sur la table

        Parameters
        ----------
        None

        Returns
        -------
        liste : list[Personnage]
        '''
        liste = []
        for i in self.personnages:
            liste.append(i.id_personnage)
        return liste
