'''
Module deplacer_personnage_vue
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

from business_object.joueur import Joueur

from dao.seance_dao import SeanceDao


class DeplacerPersonnageVue(VueAbstraite):
    def __init__(self):
        joueur = Session().user

        dict_seance = SeanceDao().lister_toutes(dict=True)

        table_list = AdministrateurService().lister_tables_actives()

        # Gros mic-mac pour replacer les tables dans l'ordre chronologique...

        liste_provisoire = []
        for t in table_list:
            listbid = t.as_list()
            listbid.append(t)
            print(len(t.personnages))
            if len(t.personnages) != 0:
                liste_provisoire.append(listbid)
                print("ajout", len(t.personnages))
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
            message = "Déplacement de personnage annulé"
            return AdministrateurMenuVue(message)

        # On recupere l id de la table d origine
        choix_fait = answers["table_origine"]
        id_table_origine = int(choix_fait.split()[7])

        # On recupere la liste des personnages de la table d origine et on les affiche
        table_origine = TableJeuService().trouver_par_id(id_table_origine)
        personnage_list = TableJeuService().lister_personnages(table_origine)
        personnage_list_affichee = [
            str(p.id_personnage) + " - " + p.nom for p in personnage_list]

        self.nettoyer_console()
        question2 = [
            {
                "type": "list",
                "name": "choix_personnage",
                "message": "Choisissez un personnage à déplacer :",
                "choices": personnage_list_affichee
            }
        ]

        # On recupere le Personnage choisi
        answers2 = prompt(question2)
        id_personnage_choisi = int(answers2["choix_personnage"].split()[0])
        personnage_choisi = PersonnageService().trouver_par_id(id_personnage_choisi)

        # On affiche les autres tables disponibles pour la meme seance
        table_arrivee_list = TableJeuService().lister(
            seance=table_origine.id_seance, complete=False)

        # on retire de la liste la table d origine et les tables sans mj
        table_arrivee_list = [
            t for t in table_arrivee_list if t.id_table != id_table_origine and t.maitre_jeu is not None]
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

        toto = answers3["table_arrivee"]
        print(toto)
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
            success = PersonnageService().quitter_table(personnage_choisi, table_origine)

            if answers3["table_arrivee"] != "Aucune table":
                success = PersonnageService().rejoindre_table(
                    id_table_arrivee_choisie, personnage_choisi)
                message = "Personnage " + personnage_choisi.nom + " déplacé de la table " + str(table_origine.id_table) + \
                    " vers la table " + str(id_table_arrivee_choisie)
            else:
                message = "Personnage supprimé de la table " + \
                    str(table_origine.id_table)

            # On receupere le joueur a partir du personnage puis on le notifie par message
            joueur_concerne = PersonnageService().trouver_joueur(personnage_choisi)
            MessageService().creer(joueur_concerne, message)

            if not success:
                message = "Déplacement de personnage échoué"
        else:
            message = "Déplacement de personnage annulé"

        return AdministrateurMenuVue(message)
