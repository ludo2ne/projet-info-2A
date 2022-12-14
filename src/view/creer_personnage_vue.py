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
from service.personnage_service import PersonnageService


class CreerPersonnageVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "input",
                "name": "nom",
                "message": "Entrez le nom de votre personnage :",
                "validate": EmptyInputValidator(),
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
            },
            {
                "type": "list",
                "name": "competence",
                "message": "Choisissez la competence de votre personnage :",
                "choices": Session().competences_personnages
            },
            {
                "type": "list",
                "name": "langue",
                "message": "Choisissez la langue de votre personnage :",
                "choices": Session().langues_personnages
            }
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        if not JoueurService().creation_personnage_autorisee():
            return JoueurMenuVue("Impossible de cr??er un nouveau personnage\n"
                                 "Vous avez d??j?? atteint le nombre maximum de "
                                 + os.environ["NB_MAX_PERSONNAGES_PAR_JOUEUR"] +
                                 " personnages autoris??s")

        joueur = Session().user

        answers = prompt(self.questions)
        message = ""

        # On appelle le service de creation de joueur
        personnage = PersonnageService().creer(answers["nom"],
                                               answers["classe"], answers["race"], answers["niveau"],
                                               competence=answers["competence"], langues_parlees=answers["langue"])

        # On r??cup??re le message ?? afficher (succ??s ou ??chec)
        if not personnage:
            message += "\nLa cr??ation du personnage a ??chou??. Vous en avez peut-??tre d??j?? un avec le m??me nom."
        else:
            joueur.liste_personnages.append(personnage)
            message += "\nLe personnage {} a bien ??t?? cr????".format(
                personnage.nom)

        return JoueurMenuVue(message)
