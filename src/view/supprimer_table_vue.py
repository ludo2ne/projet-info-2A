'''
Module supprimer_table_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from view.administrateur_menu_vue import AdministrateurMenuVue

from service.table_jeu_service import TableJeuService
from dao.seance_dao import SeanceDao


class SupprimerTableVue(VueAbstraite):
    def __init__(self):

        liste_seance = SeanceDao().lister_toutes()
        dict_seance = {}
        for s in liste_seance:
            dict_seance[str(s.id_seance)] = s.description
        self.dict_seance = dict_seance
        liste_tables_vides = TableJeuService().lister_tables_vides()
        self.liste_tables_vides = liste_tables_vides
        choix_table = []
        i = 1
        for el in liste_tables_vides:
            choix_table.append(
                f"Choix {i} : Table {el.id_table} le {dict_seance[str(el.id_seance)]}")
            i += 1
        self.tables_vides = i-1
        # ajouter à la liste la possibilité de supprimer toutes les tables vides
        choix_table.append(
            f"Choix {i} : Supprimer toutes les tables vides")

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": f"Choisissez une table parmi les {self.tables_vides} disponibles:",
                "choices": choix_table},
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Etes-vous sur(e) de vouloir cette table ou ces tables sans joueur ?"}
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):
        # Choix d'une table dans la liste des tables vides
        reponse = prompt(self.questions[0])
        choix = int(reponse["choix"].split()[1])
        if choix != self.tables_vides+1:
            liste_tables_a_supprimer = [self.liste_tables_vides[choix-1]]
        else:
            liste_tables_a_supprimer = self.liste_tables_vides

        # Si la suppression n a pas ete confirmee, on retourne au menu administrateur
        if self.tables_vides != 0:
            answers = prompt(self.questions[1])
            confirm = answers["confirmation"]
            message = ""
        else:
            confirm = False

        # La suppression est annulée en l'absence de confirmation
        if not confirm:
            message = "Suppression des tables annulée"
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = AdministrateurMenuVue(message)
        else:
            for el in liste_tables_a_supprimer:
                # On appelle le service de suppression de table
                statut_suppression = TableJeuService().supprimer(el)
                # On récupère le message à afficher (succès ou échec)
                if not statut_suppression:
                    message = "La suppression de la table {el.id_table} du {dict_seance[str(el.id_seance)]} a échoué"
                else:
                    message = f"Les tables vides de joueur ont bien été supprimées."

        return AdministrateurMenuVue(message)
