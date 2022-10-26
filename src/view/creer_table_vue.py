
from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from view.administrateur_menu_vue import AdministrateurMenuVue
from service.administrateur_service import AdministrateurService
from service.table_jeu_service import TableJeuService


class CreerTableVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "input",
                "name": "creation",
                "message": "A quelle séance souhaitez vous créer une table ?"
            },
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        answers = prompt(self.questions)
        message = ""

        if not AdministrateurService().creer_table_autorisee(answers["creation"]):
            return AdministrateurMenuVue("Impossible de créer une nouvelle table \n"
                                         "Vous avez déjà atteint le nombre maximum de table "
                                         + os.environ["NB_TABLES_MAX_PAR_SEANCE"])

        # On appelle le service de creation de joueur
        from service.table_jeu_service import TableJeuService
        table = TableJeuService().creer_table(answers["creation"])

        # On récupère le mesage à afficher (succès ou échec)
        if not table:
            message += "\nLa création de la table a échoué"
        else:
            message += "\nLa table a bien été créé à la séance " + \
                str(answers["creation"])

        return AdministrateurMenuVue(message)
