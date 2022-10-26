from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from view.administrateur_menu_vue import AdministrateurMenuVue
from service.administrateur_service import AdministrateurService


class SupprimerTableVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Etes-vous sur(e) ?"}
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
            message = "Suppression de la table annulée"
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = AdministrateurMenuVue(message)
        else:
            print("ok")
            # On appelle le service de suppression de table
            statut_suppression = AdministrateurService().supprimer_table()
            # On récupère le message à afficher (succès ou échec)
            if not statut_suppression[0]:
                #                message = "La suppression du compte a échoué"
                from view.administrateur_menu_vue import AdministrateurMenuVue
#                prochainevue = AdministrateurMenuVue(message)
                prochainevue = AdministrateurMenuVue(statut_suppression[1])
            else:
                message = f"La table a bien été supprimée. Au revoir"
                Session().user = None
                prochainevue = AdministrateurMenuVue(message)
        return prochainevue