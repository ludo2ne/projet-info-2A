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
from business_object.table_jeu import TableJeu


class RejoindreTableChoisirHoraireVue(VueAbstraite):
    def __init__(self, message):
        joueur = Session().user
        # Si une table séance est créée en base de données, chercher la correspondance des séances là-bas
        choix_horaire = ["1 Samedi matin", "2 Samedi Après-midi",
                         "3 Dimanche matin", "4 Dimanche après-midi"]

        # ajouter à la liste la possibilité de revenir en arriere sans supprimer de personnage
        choix_horaire.append("5 Non, finalement j'ai changé d'avis")

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Choisissez une plage horaire",
                "choices": choix_horaire
            },
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

        # Si l'utilisateur a changé d'avis au moment de choisir une plage horaire,
        # il retourne à la vue MenuJoueurVue
        message = ""
        if choix_fait == 5:
            message = "Choix de table annulé"
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = JoueurMenuVue(message)
        else:
            # On vérifie que le joueur est disponible sur cette plage horaire
            from service.table_jeu_service import TableJeuService
            liste_tables_jeu = TableJeuService().lister(seance=choix_fait, joueur=joueur)
            statut_libre = True
            if len(liste_tables_jeu) > 0:
                statut_libre = False
                message = "Vous jouez déjà à une table sur cette plage horaire."
                from view.joueur_menu_vue import JoueurMenuVue
                prochainevue = JoueurMenuVue(message)

            # On vérifie que le joueur n'est pas occupé en tant que MJ sur cette plage horaire
            from business_object.maitre_jeu import MaitreJeu

            if type(joueur) == MaitreJeu and statut_libre:
                from service.maitre_jeu_service import MaitreJeuService
                liste_tables_jeu_mj = MaitreJeuService().lister_tables(joueur)
                if len(liste_tables_jeu_mj) > 0:
                    for el in liste_tables_jeu_mj:
                        if el[1] == choix_fait:
                            statut_libre = False
                            message = "Vous êtes déjà Maitre du Jeu à une table sur cette plage horaire."
                            from view.joueur_menu_vue import JoueurMenuVue
                            prochainevue = JoueurMenuVue(message)
            if statut_libre:
                from view.rejoindre_table_choisir_table_vue import RejoindreTableChoisirTableVue
                message = "Vous pouvez maintenant choisir une table"
                prochainevue = RejoindreTableChoisirTableVue(
                    message, choix_fait)

        return prochainevue
