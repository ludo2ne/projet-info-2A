'''
Module lancement_appli
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


from utils.singleton import Singleton
from service.joueur_service import JoueurService
from view.accueil_vue import AccueilVue


class LancementAppli(metaclass=Singleton):
    '''
    Classe de lancement de l'application
    '''

    def lancer(self):

        vue_courante = AccueilVue()

        while vue_courante:
            try:
                # Affichage du menu
                vue_courante.display_header()

                # Affichage des choix possibles
                vue_courante = vue_courante.make_choice()
            except:
                print("Une erreur est survenue, retour au menu principal")
                vue_courante = AccueilVue()

        # Lorsque l on quitte l application
        print("---------------------------------")
        print("Au revoir")


if __name__ == '__main__':
    LancementAppli().lancer()
