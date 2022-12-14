'''
Module quitter_table_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from typing import Optional
from InquirerPy import prompt

from view.session import Session
from view.vue_abstraite import VueAbstraite
from view.joueur_menu_vue import JoueurMenuVue

from dao.table_jeu_dao import TableJeuDao
from dao.seance_dao import SeanceDao

from service.joueur_service import JoueurService
from service.personnage_service import PersonnageService
from service.table_jeu_service import TableJeuService


class QuitterTableVue(VueAbstraite):

    def __init__(self, message):
        joueur = Session().user
        # Pour le choix du joueur, afficher seulement le nom du personnage
        # et son ordre d'apparition dans la liste de personnages
        choix_table = [[t.id_seance, t.id_table, t.scenario]
                       for t in TableJeuDao().lister(joueur=joueur)]
        liste_choix = []
        i = 1
        for el in choix_table:
            seance = SeanceDao().trouver_par_id(el[0])
            el[0] = seance.description
            liste_choix.append(f"{i} {el[0]} Table {el[1]} {el[2]}")
            i += 1

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        liste_choix.append(f"{i} Non, finalement j'ai changé d'avis.")
        self.nb_choix = i

        self.questions = [
            {
                "type": "list",
                "name": "id_table",
                "message": "Choisissez une table à quitter",
                "choices": liste_choix
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
        answers = prompt(self.questions[0])

#        if not answers["confirmation"] or int(answers["id_table"][0]) == self.nb_choix:
        if int(answers["id_table"][0]) == self.nb_choix:
            return JoueurMenuVue("Aucune table quittée")

        answers2 = prompt(self.questions[1])
        if not answers2["confirmation"]:
            return JoueurMenuVue("Aucune table quittée")

        id_table_quittee = int(answers["id_table"].split()[4])
        table_quittee = TableJeuService().trouver_par_id(id_table_quittee)
        personnage_a_la_table = JoueurService(
        ).trouver_personnage_a_la_table(id_table_quittee)
        statut_suppression = PersonnageService().quitter_table(
            personnage_a_la_table, table_quittee)

        if not statut_suppression:
            message = "Le départ de la table a échoué"
        else:
            message = "Votre personnage a bien quitté la table " + \
                str(id_table_quittee)

        return JoueurMenuVue(message)
