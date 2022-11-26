'''
Module main
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

import dotenv

from view.session import Session
from view.accueil_vue import AccueilVue

from client.classe_client import ClasseClient
from client.race_client import RaceClient
from client.competence_client import CompetenceClient
from client.langue_client import LangueClient


'''
Classe de lancement de l'application
'''
if __name__ == '__main__':

    # On charge les variables d'envionnement
    dotenv.load_dotenv(override=True)

    vue_courante = AccueilVue("Bienvenue à la conférence de JDR")
    nb_erreurs = 0

    # Chargement en session de la liste des classes et des races
    Session().classes_personnages = ClasseClient().lister_classes()
    Session().races_personnages = RaceClient().lister_races()
    Session().competences_personnages = CompetenceClient().lister_competences()
    Session().langues_personnages = LangueClient().lister_langues()

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
