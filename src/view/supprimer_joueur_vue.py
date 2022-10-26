from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.administrateur_menu_vue import AdministrateurMenuVue


class SupprimerJoueurVue(VueAbstraite):
    def __init__(self):

        liste_joueur = [j.pseudo for j in JoueurService().lister_tous()]

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        liste_joueur.append("Non, finalement j'ai changé d'avis")

        self.questions = [
            {
                "type": "list",
                "name": "supression",
                "message": "Choisissez le joueur à supprimer",
                "choices": liste_joueur
            },
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Confirmez-vous ?"}
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        message = ""
        answers = prompt(self.questions)

        if not answers["confirmation"] or answers["supression"] == "Non, finalement j'ai changé d'avis":
            return AdministrateurMenuVue("Suppression de joueur annulée")
        joueur = JoueurService().trouver_par_pseudo(answers["supression"])
        statut_suppression = JoueurService().supprimer(joueur)

        if not statut_suppression[0]:
            #message = "La suppression du compte a échoué"
            from view.joueur_menu_vue import JoueurMenuVue
            #prochainevue = JoueurMenuVue(message)
            prochainevue = JoueurMenuVue(statut_suppression[1])
        else:
            message = "Le compte du joueur " + \
                str(answers["supression"]) + " a bien été supprimé."
            prochainevue = AdministrateurMenuVue(message)
        return prochainevue
