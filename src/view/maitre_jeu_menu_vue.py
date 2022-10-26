'''
Module meaitre_jeu_menu_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from service.maitre_jeu_service import MaitreJeuService
from view.session import Session


class MaitreJeuMenuVue(VueAbstraite):
    '''Menu principal d'un Maître du Jeu
    '''

    def __init__(self, message="") -> None:
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Faites votre choix",
                "choices": [
                    "Gérer une Table (TODO)",
                    "Résilier une Table",
                    "Voir les Tables gérées (TODO)",
                    "Retourner au menu Joueur",
                    "Se déconnecter"
                ]
            }
        ]
        self.message = message

    def afficher(self) -> None:
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):

        utilisateur = Session().user

        reponse = prompt(self.questions)
        if reponse["choix"] == "Retourner au menu Joueur":
            from view.joueur_menu_vue import JoueurMenuVue
            return JoueurMenuVue()
        elif reponse["choix"] == "Résilier une Table":
            message = "Vous vous apprêtez à quitter une table de jeu"
            from view.resilier_table_vue import ResilierTableVue
            return ResilierTableVue(message)
        elif reponse["choix"] == "Se déconnecter":
            Session().user = None
            from view.accueil_vue import AccueilVue
            return AccueilVue("À bientôt {}".format(utilisateur.pseudo))
