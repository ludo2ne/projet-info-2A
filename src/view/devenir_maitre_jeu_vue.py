'''
Module devenir_maitre_jeu_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 26/10/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.session import Session
from business_object.joueur import Joueur
from view.joueur_menu_vue import JoueurMenuVue


class DevenirMaitreJeuVue(VueAbstraite):

    def __init__(self, message=""):
        joueur = Session().user

        self.questions = [
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Confirmez-vous votre choix ?"}
        ]
        self.message = message

    def afficher(self):
        self.nettoyer_console()  # laisser suffisamment d'espace avec la vue precedente
        print(self.message)
        print()  # nous laisse un espace

    def choisir_menu(self):
        joueur = Session().user
        # recuperer les reponses saisies par le maitre de jeu
        answers = prompt(self.questions)
        confirm = answers["confirmation"]

        if confirm:
            message = f"Nous vous remercions pour votre participation active, {joueur.prenom}!"
            from service.maitre_jeu_service import MaitreJeuService
            statut = MaitreJeuService().devenir_mj()
        else:
            message = "Ce n'est pas grave, vous avez le temps d'y réfléchir."

        return JoueurMenuVue(message)
