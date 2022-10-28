'''
Module accueil_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from typing import Optional
from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from view.inscription_vue import InscriptionVue
from view.connexion_vue import ConnexionVue
from utils.reset_database import ResetDatabase
from utils.headers import headers


class AccueilVue(VueAbstraite):
    '''Vue de l'accueil de l'application du Jeu de Rôle.

    Attributes
    ----------
    message='' 
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisi par l'utilisateur de l'application
    '''

    def __init__(self, message="") -> None:
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Faites votre choix",
                "choices": [
                    "Créer un compte Joueur",
                    "Se connecter",
                    "Ré-initialiser la base de données",
                    "Quitter"
                ]
            }
        ]
        self.message = headers().print_header()+message

    def afficher(self) -> None:
        '''Echappe un grans espace dans le terminal pour simuler le changement de page de l'application
        '''
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        ''' Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisi par l'utilisateur dans le terminal
        '''
        reponse = prompt(self.questions)
        if reponse["choix"] == "Quitter":
            pass
        elif reponse["choix"] == "Se connecter":
            return ConnexionVue()
        elif reponse["choix"] == "Créer un compte Joueur":
            return InscriptionVue()
        elif reponse["choix"] == "Ré-initialiser la base de données":
            succes = ResetDatabase().lancer()
            message = "Ré-initilisation de la base de données terminée" if succes else None
            return AccueilVue(message)
