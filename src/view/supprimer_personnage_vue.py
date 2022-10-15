'''
Module supprimer_personnage_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.session import Session
from business_object.joueur import Joueur


class SupprimerPersonnageVue(VueAbstraite):
    def __init__(self, message):
        joueur = Session().user
        print("init SupprimerPersonnageVue")
        # Pour le choix du joueur, afficher seulement le nom du personnage
        # et son ordre d'apparition dans la liste de personnages
        choix_perso = []
        i = 1
        for perso in joueur.liste_personnages:
            print(perso.as_list())
            choix_perso.append(f"{i} {perso.nom}")
            i += 1

        # TODO ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Choisissez un personnage à supprimer",
                "choices": choix_perso
            }
        ]
        self.message = message

    def afficher(self):
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        joueur = Session().user
        answers = prompt(self.questions)

        # On récupère le personnage à supprimer
        choix_fait = int(answers["choix"][0])-1
        perso_choisi = joueur.liste_personnages[choix_fait]
        # On appelle le service de suppression de personnage
        statut_suppression = JoueurService().supprimer_personnage(perso_choisi)

        message = ""
        # On récupère le message à afficher (succès ou échec)
        if not statut_suppression:
            message = "La suppression du personnage a échoué"
        else:
            message = "Le personnage {} a bien été supprimé".format(
                perso_choisi.nom)

        from view.joueur_menu_vue import JoueurMenuVue
        return JoueurMenuVue(message)
