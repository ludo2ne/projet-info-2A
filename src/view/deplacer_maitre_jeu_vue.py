'''
Module deplacer_maitre_jeu_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.session import Session
from view.vue_abstraite import VueAbstraite
from view.administrateur_menu_vue import AdministrateurMenuVue

from service.administrateur_service import AdministrateurService
from service.table_jeu_service import TableJeuService
from service.personnage_service import PersonnageService
from service.message_service import MessageService
from service.maitre_jeu_service import MaitreJeuService
from dao.seance_dao import SeanceDao

from business_object.joueur import Joueur
from business_object.maitre_jeu import MaitreJeu


class DeplacerMaitreJeuVue(VueAbstraite):
    def __init__(self):
        joueur = Session().user

        dict_seance = SeanceDao().lister_toutes(dict=True)

        # TODO lister les tables avec un mj
        table_list = AdministrateurService().lister_tables_actives()

        # Gros mic-mac pour replacer les tables dans l'ordre chronologique...
        liste_provisoire = []
        for t in table_list:
            listbid = t.as_list()
            listbid.append(t)
            if t.maitre_jeu:
                liste_provisoire.append(listbid)
        liste_provisoire.sort()
        table_list = [t[-1] for t in liste_provisoire]

        i = 1
        table_list_affichee = []
        for t in table_list:
            table_list_affichee.append(str(i) + ". Séance " + str(t.id_seance) + ": " + dict_seance[str(t.id_seance)] +
                                       " - Table " + str(t.id_table) + " - " +
                                       str(t.scenario))
            i += 1

        self.nb_choix = i

        # ajouter a la liste la possibilite de revenir en arriere sans deplacer de personnage
        table_list_affichee.append(f"{i}. Non, finalement j'ai changé d'avis")

        self.question1 = [
            {
                "type": "list",
                "name": "table_origine",
                "message": "Choisissez la table d'origine :",
                "choices": table_list_affichee
            },
        ]
        self.message = ""
        self.table_list = table_list

    def afficher(self):
        self.nettoyer_console()
        print(self.message)
        print()

    def choisir_menu(self):
        joueur = Session().user
        answers = prompt(self.question1)

        if int(answers["table_origine"][0]) == self.nb_choix:
            message = "Déplacement du Maître du Jeu annulé"
            return AdministrateurMenuVue(message)

        # On recupere l id de la table d origine
        choix_fait = answers["table_origine"]
        id_table_origine = int(choix_fait.split()[7])

        # On recupere la liste des personnages de la table d origine et on les affiche
        table_origine = TableJeuService().trouver_par_id(id_table_origine)

        # Recuperation du Maitre du Jeu de la Table
        maitre_jeu = TableJeuService().trouver_mj(table_origine)

        # TODO lister les tables sans mj

        # On recupere la Seance
        seance = SeanceDao().trouver_par_id(table_origine.id_seance)

        # On affiche les autres tables disponibles pour la meme seance
        table_arrivee_list = MaitreJeuService().liste_tables_sans_mj(seance)

        table_arrivee_list_affichee = [
            t.id_table for t in table_arrivee_list]
        table_arrivee_list_affichee.append("Aucune table")

        table_arrivee_txt = TableJeuService().affichage_liste(table_arrivee_list)
        self.nettoyer_console()
        print(table_arrivee_txt)
        question3 = [
            {
                "type": "list",
                "name": "table_arrivee",
                "message": "Choisissez le numéro de la table d'arrivée :",
                "choices": table_arrivee_list_affichee
            },
        ]
        answers3 = prompt(question3)

        if answers3["table_arrivee"] != "Aucune table":
            id_table_arrivee_choisie = int(answers3["table_arrivee"])

        self.nettoyer_console()
        question4 = [
            {
                "type": "confirm",
                "name": "confirmation",
                "message": "Confirmez-vous ce déplacement ?"}
        ]
        answers4 = prompt(question4)
        confirm = answers4["confirmation"]

        if confirm:
            success = MaitreJeuService().resilier_table(maitre_jeu, seance.id_seance)

            if answers3["table_arrivee"] != "Aucune table":
                table_arrivee = TableJeuService().trouver_par_id(id_table_arrivee_choisie)
                success = MaitreJeuService().gerer_table(seance, table_origine.scenario,
                                                         table_origine.infos_complementaires,
                                                         maitre_jeu, table_arrivee)
                message = "Maître du Jeu " + maitre_jeu.nom + " déplacé de la table " + str(table_origine.id_table) + \
                    " vers la table " + str(id_table_arrivee_choisie)
                message_mj = "Vous avez été déplacé de la table " + str(table_origine.id_table) + " vers la table " + str(id_table_arrivee_choisie) + \
                    " en tant que MJ pour la séance de " + seance.description

            else:
                message = "Maître du Jeu supprimé de la table " + \
                    str(table_origine.id_table)
                message_mj = "Vous avez été démis de votre fonction de MJ pour la table " + \
                    str(table_origine.id_table) + \
                    " de la séance de " + seance.description

            table_origine.scenario = None
            # Message pour prevenir le maitre du jeu
            MessageService().creer(maitre_jeu, message_mj)

            if not success:
                message = "Déplacement de Maître du Jeu échoué"
        else:
            message = "Déplacement de Maître du Jeu annulé"

        return AdministrateurMenuVue(message)
