'''
Module rejoindre_table_choisir_horaire_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.session import Session
from view.vue_abstraite import VueAbstraite

from service.joueur_service import JoueurService

from dao.seance_dao import SeanceDao
from dao.table_jeu_dao import TableJeuDao

from business_object.joueur import Joueur
from business_object.table_jeu import TableJeu


class RejoindreTableChoisirHoraireVue(VueAbstraite):
    def __init__(self, message):
        joueur = Session().user

        liste_seance = SeanceDao().lister_toutes()

        # Déterminer les séances pour lesquelles le joueur-MJ est occupé
        liste_table_joueur = TableJeuDao().lister(joueur=joueur)
        liste_table_mj = TableJeuDao().lister(mj=joueur)
        liste_seance_occupe = []
        for el in liste_table_joueur:
            liste_seance_occupe.append(el.id_seance)
        for el in liste_table_mj:
            liste_seance_occupe.append(el.id_seance)

        liste_seances_affichee = []
        i = 1
        for s in liste_seance:
            if not s.id_seance in liste_seance_occupe:
                liste_seances_affichee.append(str(i)+". séance " +
                                              str(s.id_seance) + " : " + s.description)
                i += 1
        self.nb_choix = i

        # ajouter à la liste la possibilité de revenir en arriere
        liste_seances_affichee.append(
            f"{i}. Non, finalement j'ai changé d'avis")

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Choisissez une plage horaire",
                "choices": liste_seances_affichee
            }
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
        if choix_fait == self.nb_choix:
            message = "Choix de table annulé"
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = JoueurMenuVue(message)
        else:
            id_seance = int(answers["choix"].split()[2])
            # On vérifie que le joueur est disponible sur cette plage horaire
            from service.table_jeu_service import TableJeuService
            liste_tables_jeu = TableJeuService().lister(seance=id_seance, joueur=joueur)
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
                        if el[1] == id_seance:
                            statut_libre = False
                            message = "Vous êtes déjà Maitre du Jeu à une table sur cette plage horaire."
                            from view.joueur_menu_vue import JoueurMenuVue
                            prochainevue = JoueurMenuVue(message)

            # On vérifie qu'il y a des tables libres sur cette plage horaire
            liste_tables_plage = TableJeuService().lister(seance=id_seance, complete=False)
            if len(liste_tables_plage) == 0:
                statut_libre = False
                message = "Aucune table n'est disponible sur cette plage horaire. Réessayez plus tard."
                from view.joueur_menu_vue import JoueurMenuVue
                prochainevue = JoueurMenuVue(message)

            if statut_libre:
                from view.rejoindre_table_choisir_table_vue import RejoindreTableChoisirTableVue
                message = "Vous pouvez maintenant choisir une table"
                prochainevue = RejoindreTableChoisirTableVue(
                    message, id_seance)

        return prochainevue
