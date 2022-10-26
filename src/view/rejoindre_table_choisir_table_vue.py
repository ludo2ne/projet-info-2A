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
from business_object.table_jeu import TableJeu


class RejoindreTableChoisirTableVue(VueAbstraite):
    def __init__(self, message, plage_horaire):
        joueur = Session().user
        self.plage_horaire = plage_horaire
        # Si une table séance est créée, chercher la correspondance des séances là-bas
        from service.table_jeu_service import TableJeuService
        liste_tables_jeu = TableJeuService().lister(seance=plage_horaire)
        choix_table = []
        i = 1
        for el in liste_tables_jeu:
            if len(el.personnages) < el.nb_joueurs_max:
                choix_table.append(f"Choix {i} : Table {el.id_table} avec {len(el.personnages)} joueurs inscrits.\n" +
                                   f"Scénario: {el.scenario}")
            i += 1
        self.tables_libres = i-1
        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        if i > 1:
            choix_table.append(f"Choix {i} : Finalement j'ai changé d'avis.")
        else:
            choix_table.append(
                f"Choix {i} : Désolé, il n'y a pas de table libre...")

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": f"Choisissez une table parmi les {self.tables_libres} disponibles:",
                "choices": choix_table
            },
        ]
        self.message = message

    def afficher(self):
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        joueur = Session().user
        answers = prompt(self.questions[0])
        # On récupère le choix de l'utilisateur

        choix_fait = int(answers["choix"].split()[1])

        # Si l'utilisateur a changé d'avis au moment de choisir une table,
        # il retourne à la vue MenuJoueurVue
        message = ""
        if choix_fait == self.tables_libres+1:
            message = "Choix de table annulé"
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = JoueurMenuVue("message")
        else:
            table_choisie = int(answers["choix"].split()[4])
            from view.rejoindre_table_choisir_perso_vue import RejoindreTableChoisirPersoVue
            message = "Vous pouvez maintenant choisir un personnage"
            prochainevue = RejoindreTableChoisirPersoVue(
                message, table_choisie)

        return prochainevue
