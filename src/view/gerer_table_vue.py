'''
Module gerer_table_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 26/10/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService
from service.maitre_jeu_service import MaitreJeuService

from dao.seance_dao import SeanceDao
from dao.table_jeu_dao import TableJeuDao

from business_object.joueur import Joueur


class GererTableVue(VueAbstraite):

    def __init__(self, message=""):
        joueur = Session().user

        liste_seance = SeanceDao().lister_toutes()

        liste_seances_affichee = []
        i = 1
        for s in liste_seance:
            liste_seances_affichee.append(
                str(s.id_seance) + ". " + s.description)
            i += 1
        liste_seances_affichee.append(f"{i}. J'ai changé d'avis")
        self.nb_choix = i

        self.questions = [
            {   # demander la séance a rejoindre
                "type": "list",
                "name": "seance",
                "message": "Sélectionnez la séance à laquelle vous souhaitez participer :",
                "choices": liste_seances_affichee
            },
            {   # demander le scenario
                "type": "input",
                "name": "scenario",
                "message": "Indiquez le scénario que vous voulez diriger :",
                "validate": EmptyInputValidator()
            },
            {   # demander l'information complementaire
                "type": "input",
                "name": "info_comple",
                "message": "Si vous souhaitez ajouter quelque chose, écrivez ici :"
            }
        ]
        self.message = message

    def afficher(self):
        self.nettoyer_console()  # laisser suffisamment d'espace avec la vue precedente
        print(self.message)
        print()  # nous laisse un espace

    def choisir_menu(self):
        mj = Session().user
        # recuperer les reponses saisies par le maitre de jeu

        reponse = prompt(self.questions[0])
        id_seance = int(reponse["seance"][0])
        if id_seance == self.nb_choix:
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue("Pas de souci, vous avez encore le temps d'y réfléchir.")

        reponse = prompt(self.questions[1])
        scenario = reponse["scenario"]
        reponse = prompt(self.questions[2])
        info_complementaire = reponse["info_comple"]

        seance = SeanceDao().trouver_par_id(id_seance)

        resultat = MaitreJeuService().gerer_table(
            seance, scenario, info_complementaire)
        # verifier si MJ est libre pour la sceance
        if resultat == "mj non libre":  # MJ n'est pas libre
            message = "Vous êtes déjà inscrit sur une autre table pour cette séance"
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue(message)
        elif resultat == "non table libre":
            message = "Désolé, il n'y a plus de table disponible pour la séance sélectionnée, vous pouvez choisir une autre séance"
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue(message)
        elif resultat == "OK":
            # TODO ajouter à la table xxx
            message = "Vous êtes officiellement Maître du Jeu pour la séance : " + seance.description
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue(message)
