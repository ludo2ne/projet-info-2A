'''
Module creer_joueur_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from InquirerPy import prompt
from prompt_toolkit.validation import ValidationError, Validator
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService

from prompt_toolkit import document
import regex


class MailValidator(Validator):
    '''la classe MailValidator verifie si la chaine de caractere qu'on entre correspond au format de l'email
    '''

    def validate(self, document) -> None:
        ok = regex.match('^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid mail', cursor_position=len(document.text))


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
            },
            {
                'type': 'input',
                'name': 'email',
                'message': 'Entrez votre email',
                'validate': MailValidator()
            }
        ]

    def afficher(self):
        self.nettoyer_console()

    def choisir_menu(self):

        answers = prompt(self.questions)

        # On regarde si le pseudo existe deja
        joueur = JoueurService().trouver_par_pseudo(answers["pseudo"])

        if joueur:
            message = "Le pseudo est déjà utilisé. Veuillez en choisir un autre"
        else:
            # On appelle le service de creation de joueur
            joueur = JoueurService().creer(answers["pseudo"],
                                           answers["nom"], answers["prenom"], mail=answers["email"])

            # On récupère le message à afficher (succès ou échec)
            if not joueur:
                message = "La création du joueur a échoué"
            else:
                message = "Le joueur {} {} a bien été. Pour vous connecter, utilisez votre pseudo : {} ".format(
                    joueur.prenom, joueur.nom, joueur.pseudo)

        from view.accueil_vue import AccueilVue
        return AccueilVue(message)
