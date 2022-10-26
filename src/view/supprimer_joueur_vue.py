from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.administrateur_menu_vue import AdministrateurMenuVue


class SupprimerJoueurVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "input",
                "name": "supression",
                "message": "Quel est le pseudo du joueur que vous souhaitez supprimer ?"
            }
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        answers = prompt(self.questions)
        message = ""

        if not JoueurService().trouver_par_pseudo(answers["supression"]):
            return AdministrateurMenuVue("Le pseudo que vous avez renseigné n'existe pas")
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
