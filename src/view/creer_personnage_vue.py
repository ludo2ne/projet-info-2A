'''
Module creer_joueur_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

import os
from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator

from view.session import Session
from view.vue_abstraite import VueAbstraite
from view.joueur_menu_vue import JoueurMenuVue
from service.joueur_service import JoueurService


class CreerPersonnageVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "input",
                "name": "nom",
                "message": "Entrez le nom de votre personnage :"
            },
            {
                "type": "list",
                "name": "classe",
                "message": "Choisissez la classe de votre personnage :",
                "choices": Session().classes_personnages
            },
            {
                "type": "list",
                "name": "race",
                "message": "Choisissez la race de votre personnage :",
                "choices": Session().races_personnages
            },
            {
                "type": "number",
                "min_allowed": 1,
                "max_allowed": 100,
                "default": None,
                "validate": EmptyInputValidator(),
                "name": "niveau",
                "message": "Entrez le niveau de votre personnage (entre 1 et 100):"
            }
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        if not JoueurService().creation_personnage_autorisee():
            return JoueurMenuVue("Impossible de créer un nouveau personnage\n"
                                 "Vous avez déjà atteint le nombre maximum de "
                                 + os.environ["NB_MAX_PERSONNAGES_PAR_JOUEUR"] +
                                 " personnages autorisés")

        answers = prompt(self.questions)
        message = ""

        # On appelle le service de creation de joueur
        personnage = JoueurService().creer_personnage(answers["nom"],
                                                      answers["classe"], answers["race"], answers["niveau"])

        # On récupère le mesage à afficher (succès ou échec)
        if not personnage:
            message += "\nLa création du personnage a échoué"
        else:
            message += "\nLe personnage {} a bien été créé".format(
                personnage.nom)

        return JoueurMenuVue(message)
