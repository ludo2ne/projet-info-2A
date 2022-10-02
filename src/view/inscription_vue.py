'''
Module creer_joueur_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService


class InscriptionVue(VueAbstraite):
    def __init__(self):
        self.questions = [
            {
                "type": "input",
                "name": "pseudo",
                "message": "Entrez votre pseudo :"
            },
            {
                "type": "input",
                "name": "nom",
                "message": "Entrez votre nom :"
            },
            {
                "type": "input",
                "name": "prenom",
                "message": "Entrez votre prénom :"
            }
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        answers = prompt(self.questions)

        # On appelle le service de creation de joueur
        joueur = JoueurService().creer(answers["pseudo"],
                                       answers["nom"], answers["prenom"], mail=None)

        # On récupère le mesage à afficher (succès ou échec)
        if not joueur:
            message = "La création du joueur a échoué"
        else:
            message = "Le joueur {} {} a bien été créé".format(
                joueur.prenom, joueur.nom)

        from view.accueil_vue import AccueilVue
        return AccueilVue(message)
