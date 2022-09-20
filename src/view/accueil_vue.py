from typing import Optional
from InquirerPy import prompt

from view.creer_joueur_vue import CreerJoueurVue


class AccueilVue():

    def __init__(self) -> None:
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": 'Bienvenue à la conférence de JDR',
                "choices": [
                    "Créer un compte Joueur",
                    "Se connecter",
                    "Quitter"
                ]
            }
        ]

    def clear_console(self) -> None:
        for i in range(0, 50):
            print("")

    def display_header(self) -> None:
        self.clear_console()

    def make_choice(self):
        reponse = prompt(self.questions)
        if reponse["choix"] == "Quitter":
            pass
        elif reponse["choix"] == "Se connecter":
            # TODO
            pass
        elif reponse["choix"] == "Créer un compte Joueur":
            return CreerJoueurVue()
