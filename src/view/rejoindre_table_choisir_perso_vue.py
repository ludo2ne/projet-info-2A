'''
Module rejoindre_table_choisir_perso_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.personnage_service import PersonnageService
from view.session import Session
from business_object.joueur import Joueur
from business_object.table_jeu import TableJeu


class RejoindreTableChoisirPersoVue(VueAbstraite):
    def __init__(self, message, table_choisie):
        joueur = Session().user
        self.table_choisie = table_choisie
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
                "message": "Choisissez un personnage pour participer à cette table",
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
            message = "Réservation de table annulée."
        else:
            perso_choisi = joueur.liste_personnages[choix_fait-1]
            # On appelle le service de réservation de table
            statut_reservation = PersonnageService().rejoindre_table(
                self.table_choisie, perso_choisi)
            # On récupère le message à afficher (succès ou échec)
            if not statut_reservation:
                message = "La réservation de table a échoué."
            else:
                message = f"Vous êtes inscrit(e) en table {self.table_choisie} " +\
                    f"avec le personnage {perso_choisi.nom}."

        from view.joueur_menu_vue import JoueurMenuVue
        return JoueurMenuVue(message)
