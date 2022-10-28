
from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from view.administrateur_menu_vue import AdministrateurMenuVue
from service.administrateur_service import AdministrateurService
from service.table_jeu_service import TableJeuService
from dao.seance_dao import SeanceDao


class CreerTableVue(VueAbstraite):
    def __init__(self):
        liste_seance = SeanceDao().lister_toutes()

        liste_seances_affichee = []
        i = 1
        for s in liste_seance:
            liste_seances_affichee.append(
                str(s.id_seance) + ". " + s.description)
            i += 1
        self.nb_choix = i
        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        liste_seances_affichee.append(
            f"{i}. Non, finalement j'ai changé d'avis")

        self.questions = [
            {
                "type": "list",
                "name": "creation",
                "message": "A quelle séance souhaitez vous créer une table ?",
                "choices": liste_seances_affichee
            }
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        answers = prompt(self.questions)
        message = ""

        if int(answers["creation"][0]) == self.nb_choix:
            message = "Abandon de la création de table"
            return AdministrateurMenuVue(message)

        if not AdministrateurService().creer_table_autorisee(int(answers["creation"][0])):
            return AdministrateurMenuVue("Impossible de créer une nouvelle table \n"
                                         "Vous avez déjà atteint le nombre maximum de table "
                                         + os.environ["NB_TABLES_MAX_PAR_SEANCE"])

        # On appelle le service de creation de joueur
        from service.table_jeu_service import TableJeuService
        table = TableJeuService().creer_table(int(answers["creation"][0]))

        # On récupère le mesage à afficher (succès ou échec)
        if not table:
            message += "\nLa création de la table a échoué"
        else:
            message += "\nLa table a bien été créé à la séance du " + \
                answers["creation"][3::]

        return AdministrateurMenuVue(message)
