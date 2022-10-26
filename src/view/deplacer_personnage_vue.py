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

from service.administrateur_service import AdministrateurService
from service.table_jeu_service import TableJeuService

from business_object.joueur import Joueur


class DeplacerPersonnageVue(VueAbstraite):
    def __init__(self):
        joueur = Session().user
        # Pour le choix de la table, afficher seulement la séance et le scenario
        # et son ordre d'apparition dans la liste de tables
        table_list = [str(t.id_table) + " | Séance " + str(t.id_seance) + " - Table " + str(t.id_table) + " - " +
                      str(t.scenario) for t in AdministrateurService().lister_tables_actives()]

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        table_list.append("Non, finalement j'ai changé d'avis")

        self.question1 = [
            {
                "type": "list",
                "name": "table_origine",
                "message": "Choisissez une table : \n",
                "choices": table_list
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

        # On recupere l id de la table d origine
        id_table_origine = int(answers["table_origine"][0])

        # On recupere la liste des personnages de la table d origine et on les affiche
        personnage_list = TableJeuService().lister_personnages(id_table_origine)
        personnage_list_affichee = [
            p.id_personnage + " - " + p.nom for p in personnage_list]
        question2 = [
            {
                "type": "list",
                "name": "choix_personnage",
                "message": "Choisissez un personnage : \n",
                "choices": personnage_list_affichee
            }
        ]

        answers2 = prompt(question2)
        personnage_choisi = int(answers2["choix_personnage"][0])

        # TODO lister puis choisir la nouvelle table

        # TODO verifier que le joueur est bien libre a cette seance (si cela concerne une autre seance)
        #      ou pas si on considere qu on reste toujours sur la meme seance

        # TODO si tout est ok mettre a jour la bdd
