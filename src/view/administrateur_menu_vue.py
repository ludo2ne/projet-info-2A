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
                    "Lister les utilisateurs",
                    "Voir le programme complet",
                    "Déplacer un personnage",
                    "Déplacer un Maitre du Jeu",
                    "Créer une Table de Jeu",
                    "Supprimer les tables sans joueur",
                    "Supprimer un joueur",
                    "Voir les messages",
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
        if reponse["choix"] == "Lister les utilisateurs":
            message = AdministrateurService().lister_joueur()
            return (AdministrateurMenuVue(message))
        if reponse["choix"] == "Voir le programme complet":
            programme = AdministrateurService().voir_programme_complet()
            return (AdministrateurMenuVue(programme))
        elif reponse["choix"] == "Déplacer un personnage":
            from view.deplacer_personnage_vue import DeplacerPersonnageVue
            return DeplacerPersonnageVue()
        elif reponse["choix"] == "Déplacer un Maitre du Jeu":
            from view.deplacer_maitre_jeu_vue import DeplacerMaitreJeuVue
            return DeplacerMaitreJeuVue()
        elif reponse["choix"] == "Créer une Table de Jeu":
            from view.creer_table_vue import CreerTableVue
            return CreerTableVue()
        elif reponse["choix"] == "Supprimer les tables sans joueur":
            from view.supprimer_table_vue import SupprimerTableVue
            return SupprimerTableVue()
        elif reponse["choix"] == "Supprimer un joueur":
            from view.supprimer_joueur_vue import SupprimerJoueurVue
            return SupprimerJoueurVue()
        elif reponse["choix"] == "Voir les messages":
            msg = AdministrateurService().voir_messages()
            return (AdministrateurMenuVue(msg))
        elif reponse["choix"] == "Se déconnecter":
            Session().user = None
            from view.accueil_vue import AccueilVue
            return AccueilVue("À bientôt admin")
