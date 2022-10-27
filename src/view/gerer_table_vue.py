'''
Module supprimer_personnage_vue
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

from business_object.joueur import Joueur


class GererTableVue(VueAbstraite):

    def __init__(self, message=""):
        joueur = Session().user

        liste_seance = SeanceDao().lister_toutes()

        liste_seances_affichee = []
        for s in liste_seance:
            liste_seances_affichee.append(
                str(s.id_seance) + ". " + s.description)

        self.questions = [
            {   # demander le séance a rejoindre
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
        reponse = prompt(self.questions)
        id_seance = int(reponse["seance"][0])
        scenario = reponse["scenario"]
        info_complementaire = reponse["info_comple"]

        seance = SeanceDao().trouver_par_id(id_seance)

        resultat = MaitreJeuService().gerer_table(
            seance, scenario, info_complementaire)
        # verifier si MJ est libre pour la sceance
        if resultat == "mj non libre":  # MJ n'est pas libre
            message = "Vous ne pouvez pas jouer à tables en même temps, veuillez vérifier pour quelle table vous vous êtes inscrit et la séance correspondant"
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue(message)
        elif resultat == "non table libre":
            message = "Désolé, il n'y a plus de tables disponibles pour la séance que vous avez sélectionnée, veuillez choisir une nouvelle séance"
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue(message)
        elif resultat == "OK":
            # TODO ajouter à la table xxx
            message = "Vous êtes officiellement Maître du Jeu pour la séance : " + seance.description
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue(message)
