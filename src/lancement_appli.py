'''
Module lancement_appli
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
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

        vue_courante = AccueilVue("Bienvenue à la conférence de JDR")
        nb_erreurs = 0

        while vue_courante:
            if nb_erreurs > 100:
                print("Le programme recense trop d'erreurs et va s'arrêter")
                break
            try:
                # Affichage du menu
                vue_courante.afficher()

                # Affichage des choix possibles
                vue_courante = vue_courante.choisir_menu()
            except:
                nb_erreurs += 1
                vue_courante = AccueilVue(
                    "Une erreur est survenue, retour au menu principal")

        # Lorsque l on quitte l application
        print("---------------------------------")
        print("Au revoir")


if __name__ == '__main__':
    LancementAppli().lancer()
