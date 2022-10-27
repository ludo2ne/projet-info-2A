'''
Module lancement_appli
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from utils.singleton import Singleton

from view.session import Session
from service.joueur_service import JoueurService
from view.accueil_vue import AccueilVue
from client.classe_client import ClasseClient
from client.race_client import RaceClient
from client.competence_client import CompetenceClient
from client.langue_client import LangueClient


class LancementAppli(metaclass=Singleton):
    '''
    Classe de lancement de l'application
    '''

    def lancer(self):

        vue_courante = AccueilVue("Bienvenue à la conférence de JDR")
        nb_erreurs = 0

        # Chargement en session de la liste des classes et des races
        Session().classes_personnages = ClasseClient().lister_classes()
        Session().races_personnages = RaceClient().lister_races()
        Session().competences_personnages = CompetenceClient().lister_competences()
        Session().langues_personnages = LangueClient().lister_langues()

        # TODO prévoir solution de contournement si le webservice n'est pas accessible

        while vue_courante:
            if nb_erreurs > 100:
                print("Le programme recense trop d'erreurs et va s'arrêter")
                break
            try:
                # Affichage du menu
                vue_courante.afficher()

                # Affichage des choix possibles
                vue_courante = vue_courante.choisir_menu()
            except Exception as e:
                print(e)
                nb_erreurs += 1
                vue_courante = AccueilVue(
                    "Une erreur est survenue, retour au menu principal")

        # Lorsque l on quitte l application
        print("---------------------------------")
        print("Au revoir")


if __name__ == '__main__':
    LancementAppli().lancer()
