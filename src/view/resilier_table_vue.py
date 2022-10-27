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
from service.maitre_jeu_service import MaitreJeuService
from view.session import Session
from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
from business_object.joueur import Joueur


class ResilierTableVue(VueAbstraite):
    def __init__(self, message):
        joueur = Session().user
        # Pour le choix de la table, afficher seulement la séance et le scenario
        # et son ordre d'apparition dans la liste de tables
        table_list = MaitreJeuService().lister_tables(joueur)
        choix_table = []
        i = 1
        for el in table_list:
            choix_table.append(f"{i} {el[2]}")
            i += 1

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        choix_table.append(f"{i} Non, finalement j'ai changé d'avis")

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Choisissez une table à quitter:\n" +
                "Séance   Scénario",
                "choices": choix_table
            },
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Confirmez-vous ?"}
        ]
        self.message = message
        self.table_list = table_list

    def afficher(self):
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        joueur = Session().user
        answers = prompt(self.questions[0])
        # On récupère le choix de l'utilisateur
        choix_fait = int(answers["choix"][0])

        # Si une table a été choisie, on demande confirmation
        confirm = False
        if choix_fait != len(self.table_list)+1:
            # Si la suppression n a pas ete confirmee, on retourne au menu MaitreJeu
            answers = prompt(self.questions[1])
            confirm = answers["confirmation"]
            message = ""

        # Deux cas de figures entrainent l'annulation de la procédure et
        # le retour au menu MaitreJeu:
        # 1) l'utilisateur a changé d'avis au moment de choisir une table
        # 2) Il n'a pas confirmé son choix
        if not confirm or choix_fait == len(self.table_list)+1:
            message = "Résiliation de table annulée"
        else:
            table_choisie = self.table_list[choix_fait-1]

            # On appelle le service de résiliation de table
            statut_suppression = MaitreJeuService(
            ).quitter_table(joueur, table_choisie[1])
            # On récupère le message à afficher (succès ou échec)
            if not statut_suppression[0]:
                message = statut_suppression[1] + \
                    f"{statut_suppression[1]}\n La résiliation de table a échoué"
            else:
                message = statut_suppression[1] + \
                    f"Vous avez bien quitté la table {table_choisie} ."

        return MaitreJeuMenuVue(message)
