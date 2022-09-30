'''
Module menu_joueur_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.session import Session


class JoueurMenuVue(VueAbstraite):
    '''Menu principal d'un joueur
    '''

    def __init__(self, message="") -> None:
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Faites votre choix",
                "choices": [
                    "Créer un personnage",
                    "Supprimer un personnage",
                    "Lister ses personnages",
                    "Rejoindre une table",
                    "Quitter une table",
                    "Voir son programme",
                    "Supprimer son compte",
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
        if reponse["choix"] == "Créer un personnage":
            pass
        elif reponse["choix"] == "Se déconnecter":
            from view.accueil_vue import AccueilVue
            return AccueilVue("À bientôt {}".format(utilisateur.pseudo))