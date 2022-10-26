'''
Module menu_joueur_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService
from service.administrateur_service import AdministrateurService


class AdministrateurMenuVue(VueAbstraite):
    '''Menu principal de l'administrateur
    '''

    def __init__(self, message="") -> None:
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Faites votre choix",
                "choices": [
                    "Voir le programme complet",
                    "Déplacer un personnage (TODO)",
                    "Déplacer un Maitre du Jeu (TODO)",
                    "Créer une Table de Jeu",
                    "Supprimer une Table de Jeu (TODO)",
                    "Supprimer un joueur (TODO)",
                    "Voir les messages (TODO)",
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

        reponse = prompt(self.questions)
        if reponse["choix"] == "Voir le programme complet":
            programme = AdministrateurService().voir_programme_complet()
            return (AdministrateurMenuVue(programme))
        elif reponse["choix"] == "Déplacer un joueur":
            pass
        elif reponse["choix"] == "Créer une Table de Jeu":
            print("ok")
            from view.creer_table_vue import CreerTableVue
            return CreerTableVue()
        elif reponse["choix"] == "Supprimer un joueur":
            pass
        elif reponse["choix"] == "Voir les messages":
            pass
        elif reponse["choix"] == "Se déconnecter":
            Session().user = None
            from view.accueil_vue import AccueilVue
            return AccueilVue("À bientôt admin")
