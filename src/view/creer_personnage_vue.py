'''
Module creer_joueur_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService


class CreerPersonnageVue(VueAbstraite):
    def __init__(self):

        liste_races = ["Humain", "Nain", "Elfe"]
        liste_classes = ["Humain", "Nain", "Elfe"]

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
                "choices": liste_classes
            },
            {
                "type": "list",
                "name": "race",
                "message": "Choisissez la race de votre personnage :",
                "choices": liste_races
            },
            {
                "type": "number",
                "min_allowed": 1,
                "max_allowed": 100,
                "default": 1,
                "name": "niveau",
                "message": "Entrez le niveau de votre personnage (entre 1 et 100):"
            }
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        answers = prompt(self.questions)

        # On appelle le service de creation de joueur
        personnage = JoueurService().creer_personnage(answers["nom"],
                                                      answers["classe"], answers["race"], answers["niveau"])

        # On récupère le mesage à afficher (succès ou échec)
        if not personnage:
            message = "La création du personnage a échoué"
        else:
            message = "Le personnage {} a bien été créé".format(
                personnage.nom)

        from view.joueur_menu_vue import JoueurMenuVue
        return JoueurMenuVue(message)
