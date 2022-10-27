'''
Module quitter_table_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from typing import Optional
from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from dao.table_jeu_dao import TableJeuDao


class QuitterTableVue(VueAbstraite):

    def __init__(self, message):
        joueur = Session().user
        # Pour le choix du joueur, afficher seulement le nom du personnage
        # et son ordre d'apparition dans la liste de personnages
        choix_table = [t.id_table for t in TableJeuDao().lister(joueur=joueur)]

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        choix_table.append("Non, finalement j'ai changé d'avis")

        self.questions = [
            {
                "type": "list",
                "name": "id_table",
                "message": "Choisissez une table à quitter",
                "choices": choix_table
            },
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Confirmez-vous ?"}
        ]
        self.message = message

    def afficher(self):
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        message = ""
        answers = prompt(self.questions)

        if not answers["confirmation"] or answers["choix"] == "Non, finalement j'ai changé d'avis":
            return JoueurMenuVue("Aucune table quittée")

        statut_suppression = JoueurService().quitter_table(answers["id_table"])

        if not statut_suppression[0]:
            # message = "La suppression du compte a échoué"
            from view.joueur_menu_vue import JoueurMenuVue
            # prochainevue = JoueurMenuVue(message)
            prochainevue = JoueurMenuVue(statut_suppression[1])
        else:
            message = "Le compte du joueur " + \
                str(answers["supression"]) + " a bien été supprimé."
            prochainevue = AdministrateurMenuVue(message)
        return prochainevue
