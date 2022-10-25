'''
Module supprimer_personnage_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.session import Session
from business_object.joueur import Joueur


class SupprimerCompteVue(VueAbstraite):
    def __init__(self, message):
        joueur = Session().user
        # Demander confirmation de la suppression du compte
        self.questions = [
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Etes-vous sur(e) ?"}
        ]
        self.message = message

    def afficher(self):
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        joueur = Session().user
        # Si la suppression n a pas ete confirmee, on retourne au menu joueur
        answers = prompt(self.questions)
        confirm = answers["confirmation"]
        message = ""

        # La suppression est annulée en l'absence de confirmation
        if not confirm:
            message = "Suppression du compte annulée"
        else:
            # On appelle le service de suppression de compte
            statut_suppression = JoueurService().supprimer(joueur)
            # On récupère le message à afficher (succès ou échec)
            if not statut_suppression:
                message = "La suppression du compte a échoué"
                from view.joueur_menu_vue import JoueurMenuVue
                prochainevue = JoueurMenuVue(message)
            else:
                message = f"Votre compte a bien été supprimé. Au revoir {joueur.prenom}"
                from view.accueil_vue import AccueilVue
                prochainevue = AccueilVue(message)
        return prochainevue
