'''
Module lancement_appli
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


from service.joueur_service import JoueurService


class LancementAppli:
    '''
    Classe de lancement de l'application
    '''

    def __init__(self):
        # TODO choix = 1 : s'inscrire ou 2 : se connecter
        choix = 1
        if choix == 1:
            # TODO questionnaire
            JoueurService.creer(nom, prenom)
