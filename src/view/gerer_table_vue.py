'''
Module supprimer_personnage_vue
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


class s(VueAbstraite):
    def __init__(self, message=""):
        joueur = Session().user
        # demander la séance a rejoindre
        self.questions = [
            {
                "type": "input",
                "name": "seance",
                "message": "A quelles séance assistez-vous ?"}
        ]
        # demander le scenario et info complement

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
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = JoueurMenuVue(message)
        else:
            # On appelle le service de suppression de compte
            statut_suppression = JoueurService().supprimer(joueur)
            # On récupère le message à afficher (succès ou échec)
            if not statut_suppression[0]:
                #                message = "La suppression du compte a échoué"
                from view.joueur_menu_vue import JoueurMenuVue
#                prochainevue = JoueurMenuVue(message)
                prochainevue = JoueurMenuVue(statut_suppression[1])
            else:
                message = f"Votre compte a bien été supprimé. Au revoir {joueur.prenom}"
                Session().user = None
                from view.accueil_vue import AccueilVue
                prochainevue = AccueilVue(message)
        return prochainevue
