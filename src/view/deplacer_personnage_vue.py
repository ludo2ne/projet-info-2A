'''
Module supprimer_personnage_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.session import Session
from view.vue_abstraite import VueAbstraite
from view.administrateur_menu_vue import AdministrateurMenuVue

from service.administrateur_service import AdministrateurService
from service.table_jeu_service import TableJeuService
from service.personnage_service import PersonnageService

from business_object.joueur import Joueur


class DeplacerPersonnageVue(VueAbstraite):
    def __init__(self):
        joueur = Session().user

        table_list = AdministrateurService().lister_tables_actives()
        table_list_affichee = [str(t.id_table) + " | Séance " + str(t.id_seance) + " - Table " + str(t.id_table) + " - " +
                               str(t.scenario) for t in table_list]

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        table_list_affichee.append("Non, finalement j'ai changé d'avis")

        self.question1 = [
            {
                "type": "list",
                "name": "table_origine",
                "message": "Choisissez la table d'origine : \n",
                "choices": table_list_affichee
            },
        ]
        self.message = ""
        self.table_list = table_list

    def afficher(self):
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        joueur = Session().user
        answers = prompt(self.question1)

        if answers["table_origine"] == "Non, finalement j'ai changé d'avis":
            message = "Déplacement de personnage annulé"
            return AdministrateurMenuVue(message)

        # On recupere l id de la table d origine
        id_table_origine = int(answers["table_origine"][0])

        # On recupere la liste des personnages de la table d origine et on les affiche
        table_origine = TableJeuService().trouver_par_id(id_table_origine)
        personnage_list = TableJeuService().lister_personnages(table_origine)
        personnage_list_affichee = [
            str(p.id_personnage) + " - " + p.nom for p in personnage_list]

        self.nettoyer_console()
        question2 = [
            {
                "type": "list",
                "name": "choix_personnage",
                "message": "Choisissez un personnage à déplacer : \n",
                "choices": personnage_list_affichee
            }
        ]

        # On recupere le Personnage choisi
        answers2 = prompt(question2)
        id_personnage_choisi = int(answers2["choix_personnage"][0])
        personnage_choisi = PersonnageService().trouver_par_id(id_personnage_choisi)

        # On affiche les autres tables disponibles pour la meme seance
        table_arrivee_list = TableJeuService().lister(
            seance=table_origine.id_seance, complete=False)
        table_arrivee_list_affichee = [
            t.id_table for t in table_arrivee_list]

        # on retire de la liste la table d origine
        table_arrivee_list_affichee.remove(id_table_origine)

        self.nettoyer_console()
        question3 = [
            {
                "type": "list",
                "name": "table_arrivee",
                "message": "Choisissez la table d'arrivée : \n",
                "choices": table_arrivee_list_affichee
            },
        ]
        answers3 = prompt(question3)

        id_table_arrivee_choisie = int(answers3["table_arrivee"])
        table_arrivee_choisie = TableJeuService().trouver_par_id(id_table_arrivee_choisie)

        self.nettoyer_console()
        question4 = [
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Confirmez-vous ce déplacement ?"}
        ]
        answers4 = prompt(question4)
        confirm = answers4["confirmation"]

        if confirm:
            # TODO supprimer de l ancienne table
            success = PersonnageService().rejoindre_table(
                table_arrivee_choisie, personnage_choisi)
            if success:
                message = "Personnage déplacé"
            else:
                message = "Déplacement de personnage  échoué"
        else:
            message = "Déplacement de personnage annulé"

        return AdministrateurMenuVue(message)
