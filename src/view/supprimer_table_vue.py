'''
Module supprimer_table_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from view.administrateur_menu_vue import AdministrateurMenuVue

from service.table_jeu_service import TableJeuService


class SupprimerTableVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Etes-vous sur(e) de vouloir supprimer toutes les tables sans joueur ?"}
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):
        # Si la suppression n a pas ete confirmee, on retourne au menu administrateur
        answers = prompt(self.questions)
        confirm = answers["confirmation"]
        message = ""

        # La suppression est annulée en l'absence de confirmation
        if not confirm:
            message = "Suppression des tables annulée"
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = AdministrateurMenuVue(message)
        else:
            # On appelle le service de suppression de table
            statut_suppression = TableJeuService().supprimer()
            # On récupère le message à afficher (succès ou échec)
            if not statut_suppression:
                message = "La suppression des tables a échoué"
            else:
                message = f"Les tables vides de joueur ont bien été supprimés."

        return AdministrateurMenuVue(message)
