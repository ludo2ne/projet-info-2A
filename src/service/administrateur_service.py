'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

import os
from tabulate import tabulate
from typing import List, Optional

from view.session import Session

from business_object.joueur import Joueur
from business_object.personnage import Personnage
from business_object.table_jeu import TableJeu

from dao.joueur_dao import JoueurDao
from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao
from dao.seance_dao import SeanceDao
from dao.message_dao import MessageDao


class AdministrateurService():
    '''Classe service de l'administrateur

    Attributes
    ----------
    None

    Methods
    -------
    creer_table_autorisee(seance : int) : bool
    voir_programme_complet() : str
    lister_tables_actives(self) : list[TableJeu]
    '''

    def creer_table_autorisee(self, seance) -> bool:
        '''Dit si le joueur n'a pas atteint le nombre maximum de Personnages

        Parameters
        ----------
        seance : int
            numéro de la séance

        Returns
        -------
        bool
        '''
        print("Service : Creer table autorisee")
        nb_tables = TableJeuDao().compter_tables_par_seance(seance)
        print(nb_tables)
        return nb_tables < int(os.environ["NB_TABLES_MAX_PAR_SEANCE"])

    def voir_programme_complet(self) -> str:
        '''Affiche un résumé complet des informations des tables de jeu

        Parameters
        ----------
        None

        Returns
        -------
        resultat : str
        '''

        print("Service : Voir programme complet")

        liste_tables = TableJeuDao().lister()

        entetes = ["Séance", "Numéro", "Scénario",
                   "Maître du Jeu"]

        tables_as_list = [t.as_list() for t in liste_tables]

        resultat = "Liste des tables \n" + tabulate(tabular_data=tables_as_list,
                                                    headers=entetes,
                                                    tablefmt="psql",
                                                    floatfmt=".2f") + "\n"

        sceance_courante = None
        table_txt = ""

        for t in liste_tables:

            # Si on est dans une nouvelle seance
            if not sceance_courante or t.id_seance != sceance_courante.id_seance:
                sceance_courante = SeanceDao().trouver_par_id(t.id_seance)
                table_txt += "\n###########################################################################################"
                table_txt += "\nSéance " + str(sceance_courante.id_seance)
                table_txt += " " + sceance_courante.description
                table_txt += "\n###########################################################################################\n"

            table_txt += "\nTable " + str(t.id_table)
            table_txt += "\n-------\n\n"

            if t.maitre_jeu:
                table_txt += "Maître du jeu : " + t.maitre_jeu.prenom + " "
                table_txt += t.maitre_jeu.nom + \
                    " (" + t.maitre_jeu.pseudo + ")\n"

            if t.scenario:
                table_txt += "Scénario : " + t.scenario + "\n"

            if t.personnages != []:
                entetes = ["id", "Nom", "Classe",
                           "Race", "Niveau", "Competence", "Langue parlée", "Joueur"]
                personnages_as_list = [p.as_list() for p in t.personnages]

                for p in personnages_as_list:
                    current_perso = PersonnageDao().trouver_par_id(p[0])
                    joueur = PersonnageDao().trouver_joueur(current_perso)
                    p.append(joueur.prenom + " " + joueur.nom +
                             " (" + joueur.pseudo + ")")

                table_txt += "Liste des personnages :\n" + tabulate(tabular_data=personnages_as_list,
                                                                    headers=entetes,
                                                                    tablefmt="psql",
                                                                    floatfmt=".2f") + "\n"

        print("Service : Voir programme complet - Terminé")

        resultat += table_txt

        return resultat

    def lister_tables_actives(self) -> list[TableJeu]:
        '''Retourne la liste de toutes les tables de jeu

        Parameters
        ----------
        None

        Returns
        -------
        liste_tables : list[TableJeu]
        '''

        print("Service : Lister les tables actives")
        liste_tables = TableJeuDao().lister_tables_actives()
        print("Service : Lister les tables actives - Terminé")

        return liste_tables

    def lister_joueur(self) -> str:
        print("Service : lister tous les utilisateurs")

        # recuperer les info des tous les joueurs
        informations = JoueurDao().lister_tous()

        # mettre en forme
        entetes = ["pseudo", "nom", "prenom", "mail", "est mj"]
        info_as_list = []

        for info in informations:
            listbid = info[1].as_list()
            listbid.append(info[0])
            info_as_list.append(listbid)

        resultat = "La liste des joueurs :\n" + tabulate(tabular_data=info_as_list,
                                                         headers=entetes,
                                                         tablefmt="psql",
                                                         floatfmt=".2f") + "\n"

        print("Service : lister tous les utilisateurs - Terminé")

        return resultat

    def voir_messages(self) -> str:
        '''Afficher les messages envoyés à l'administrateur

        Parameters
        ----------
        None

        Returns
        -------
        resultat : str
            renvoie le résumé des messages du joueur
        '''

        print("Service : voir les messages")

        joueur = Session().user

        messages = MessageDao().lister_admin(joueur)

        entetes = ["id_message", "id_admin", "Contenu", "Lu", "Date_création"]
        message_as_list = [msg.as_list() for msg in messages]

        resultat = "Votre Messages \n" + tabulate(tabular_data=message_as_list,
                                                  headers=entetes,
                                                  tablefmt="psql",
                                                  floatfmt=".2f") + "\n"

        print("Service : voir les messages - Terminé")

        return resultat

    def nb_messages_non_lus(self) -> int:
        '''Afficher le nombre de messages non lus

        Parameters
        ----------
        None

        Returns
        -------
        resultat : int
            renvoie le nombre de messages non lus
        '''

        print("Service : nombre de messages non lus")

        joueur = Session().user

        messages = MessageDao().lister_admin(joueur, lu=False)

        print("Service : nombre de messages non lus - Terminé")

        return len(messages)
