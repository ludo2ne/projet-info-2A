'''
Module menu_joueur_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.session import Session


class JoueurMenuVue(VueAbstraite):
    '''Menu principal d'un joueur
    '''

    def __init__(self, message="") -> None:
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Faites votre choix",
                "choices": [
                    "Créer un personnage",
                    "Supprimer un personnage",
                    "Lister ses personnages",
                    "Rejoindre une table",
                    "Quitter une table (TODO)",
                    "Voir son programme",
                    "Supprimer son compte",
                    "Voir ses messages",
                    "Se déconnecter"
                ]
            }
        ]
        self.message = message

    def afficher(self) -> None:
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):

        utilisateur = Session().user

        # Si le joueur est aussi Maitre du Jeu on affiche le lien pour acceder au menu MJ
        if utilisateur.__class__.__name__ == "MaitreJeu":
            self.questions[0].get("choices").insert(-1,
                                                    "Accéder au Menu Maître du Jeu")

        reponse = prompt(self.questions)
        if reponse["choix"] == "Créer un personnage":
            from view.creer_personnage_vue import CreerPersonnageVue
            return CreerPersonnageVue()
        elif reponse["choix"] == "Lister ses personnages":
            perso = JoueurService().lister_personnages()
            return (JoueurMenuVue(perso))
        elif reponse["choix"] == "Rejoindre une table":
            from view.rejoindre_table_choisir_horaire_vue import RejoindreTableChoisirHoraireVue
            message = "Vous allez pouvoir choisir une table pour jouer"
            return (RejoindreTableChoisirHoraireVue(message))
        elif reponse["choix"] == "Supprimer un personnage":
            message = JoueurService().lister_personnages()
            if len(utilisateur.liste_personnages) > 0:
                from view.supprimer_personnage_vue import SupprimerPersonnageVue
                prochainevue = SupprimerPersonnageVue(message)
            else:
                message = "Suppression impossible: vous n'avez pas de personnage!"
                prochainevue = JoueurMenuVue(message)
            return (prochainevue)
        elif reponse["choix"] == "Voir son programme":
            programme_txt = JoueurService().voir_son_programme()
            return (JoueurMenuVue(programme_txt))
        elif reponse["choix"] == "Supprimer son compte":
            message = "Attention! Vous êtes sur le point de supprimer votre compte."
            from view.supprimer_compte_vue import SupprimerCompteVue
            return (SupprimerCompteVue(message))
        elif reponse["choix"] == "Accéder au Menu Maître du Jeu":
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue("Bienvenue dans le menu du Maître du Jeu")
        elif reponse["choix"] == "Se déconnecter":
            Session().user = None
            from view.accueil_vue import AccueilVue
            return AccueilVue("À bientôt {}".format(utilisateur.pseudo))
        elif reponse["choix"] == "Voir ses messages":
            msg = JoueurService().voir_messages()
            return (JoueurMenuVue(msg))
