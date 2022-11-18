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

from service.personnage_service import PersonnageService

from business_object.joueur import Joueur


class SupprimerPersonnageVue(VueAbstraite):
    def __init__(self, message):
        joueur = Session().user
        # Pour le choix du joueur, afficher seulement le nom du personnage
        # et son ordre d'apparition dans la liste de personnages
        choix_perso = []
        i = 1
        for perso in joueur.liste_personnages:
            print(perso.as_list())
            choix_perso.append(f"{i} {perso.nom}")
            i += 1

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        choix_perso.append(f"{i} Non, finalement j'ai changé d'avis")

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Choisissez un personnage à supprimer",
                "choices": choix_perso
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
        joueur = Session().user
        answers = prompt(self.questions[0])
        # On récupère le choix de l'utilisateur
        choix_fait = int(answers["choix"][0])

        # Si un personnage a été choisi, on demande confirmation
        confirm = False
        if choix_fait != len(joueur.liste_personnages)+1:
            # Si la suppression n a pas ete confirmee, on retourne au menu joueur
            answers = prompt(self.questions[1])
            confirm = answers["confirmation"]
            message = ""

        # Deux cas de figures entrainent l'annulation de la procédure et
        # le retour au menu joueur:
        # 1) l'utilisateur a changé d'avis au moment de choisir un personnage
        # 2) Il n'a pas confirmé son choix
        if not confirm or choix_fait == len(joueur.liste_personnages)+1:
            message = "Suppression du Personnage annulée"
        else:
            perso_choisi = joueur.liste_personnages[choix_fait-1]
            # On appelle le service de suppression de personnage
            statut_suppression = PersonnageService().supprimer(perso_choisi, joueur)
            # On récupère le message à afficher (succès ou échec)
            if not statut_suppression[0]:
                message = f"{statut_suppression[1]}\n La suppression du personnage a échoué"
            else:
                message = "Le personnage {} a bien été supprimé".format(
                    perso_choisi.nom)

        from view.joueur_menu_vue import JoueurMenuVue
        return JoueurMenuVue(message)
