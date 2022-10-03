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
from view.session import Session


class ConnexionVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "input",
                "name": "pseudo",
                "message": "Entrez votre pseudo :"
            }
        ]

    def afficher(self):
        self.nettoyer_console()
        print("Connexion à l'application")
        print()

    def choisir_menu(self):

        answers = prompt(self.questions)

        # On appelle le service pour trouver le joueur
        joueur = JoueurService().trouver_par_pseudo(answers["pseudo"])

        # On récupère le mesage à afficher (succès ou échec)
        if not joueur:
            message = "Aucun joueur trouvé avec le pseudo " + answers["pseudo"]
            from view.accueil_vue import AccueilVue
            return AccueilVue(message)
        else:
            message = "Bienvenue " + answers["pseudo"]
            Session().user = joueur
            from view.joueur_menu_vue import JoueurMenuVue
            return JoueurMenuVue(message)
