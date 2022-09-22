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
from view.creer_joueur_vue import CreerJoueurVue


class AccueilVue(VueAbstraite):

    def __init__(self) -> None:
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Bienvenue à la conférence de JDR",
                "choices": [
                    "Créer un compte Joueur",
                    "Se connecter",
                    "Quitter"
                ]
            }
        ]

    def afficher(self) -> None:
        self.nettoyer_console()

    def choisir_menu(self):
        reponse = prompt(self.questions)
        if reponse["choix"] == "Quitter":
            pass
        elif reponse["choix"] == "Se connecter":
            # TODO
            print("Fonctionalité non implémentée")
            pass
        elif reponse["choix"] == "Créer un compte Joueur":
            return CreerJoueurVue()
