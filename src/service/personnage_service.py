'''
Module personnage_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from view.session import Session

from business_object.table_jeu import TableJeu
from business_object.personnage import Personnage
from business_object.joueur import Joueur

from dao.table_jeu_dao import TableJeuDao
from dao.personnage_dao import PersonnageDao


class PersonnageService:
    ''' Classe des services des personnages

    Methods
    -------        
    creer(nom : str, classe : str, race : str, niveau : int, competence : str, langues_parlees : str) : Personnage
    supprimer(perso_a_supprimer : Personnage, joueur : Joueur) : list[bool,str]
    trouver_par_id(id_personnage : int) : Personnage
    trouver_joueur(personnage : Personnage) : Joueur
    rejoindre_table(table : TableJeu, personnage : Personnage) : bool
    quitter_table(table : TableJeu, personnage : Personnage): bool
    '''

    def creer(self, nom, classe, race, niveau, competence, langues_parlees) -> Personnage:
        '''Service de création d'un personnage

        Parameters
        ----------
        nom : str
            nom du personnage
        classe : str
            classe du personnage
        race : str
            race du personnage
        niveau : int
            niveau du personnage
        competence : str
            competence du personnage
        langues_parlees : str
            langue du personnage

        Returns
        -------
        perso : Personnage
            retourne le personnage crée
        '''
        print("Service : Création de personnage")

        joueur = Session().user
        # verifier que le nom du personnage n'existe pas déjà
        liste_perso = PersonnageDao().lister_par_joueur(joueur)
        liste_nom_perso = [p.nom for p in liste_perso]
        if nom in liste_nom_perso:
            perso = None
            return perso

        perso = Personnage(id_personnage=None,
                           nom=nom,
                           classe=classe,
                           race=race,
                           niveau=niveau,
                           competence=competence,
                           langues_parlees=langues_parlees
                           )

        created = PersonnageDao().creer(perso)

        print("Service : Création de personnage - Terminé")

        return perso

    def supprimer(self, perso_a_supprimer, joueur=None) -> list[bool, str]:
        '''Supprimer un personnage d'un utilisateur

        Parameters
        ----------
        perso_a_supprimer : Personnage
            personnage à supprimer
        joueur : Joueur
            joueur qui possède le personnage à supprimer

        Returns
        -------
        statut_suppression : list[bool,str]
        '''
        print("Service : Suppression d'un personnage")

        if not joueur:
            joueur = Session().user

        # vérifier si le personnage n'est pas assis à une table
        perso_non_utilise = (
            PersonnageDao().lister_tables(perso_a_supprimer) == 0)

        if perso_non_utilise:
            statut_suppression = [
                PersonnageDao().supprimer(perso_a_supprimer), ""]

            # Supprimer le personnage de la liste du joueur
            for el in joueur.liste_personnages:
                print(el.nom)
            joueur.liste_personnages.remove(perso_a_supprimer)
        else:
            statut_suppression = [
                False, f"Le personnage {perso_a_supprimer.nom} est déjà utilisé sur une table.\n"]

        print("Service : Suppression de personnage - Terminé")

        return statut_suppression

    def trouver_par_id(self, id_personnage) -> Personnage:
        '''Trouver un personnage grace à son id
        Parameters
        ------
        id_personnage : int
            id du personnage recherché

        Returns
        -------
        Personnage
        '''
        print("Service : trouver Personnage à partir de son id")
        personnage = PersonnageDao().trouver_par_id(id_personnage)
        print("Service : trouver Personnage à partir de son id - Terminé")
        return personnage

    def trouver_joueur(self, personnage) -> Joueur:
        '''Trouver le joueur à qui appartient le Personnage
        Params
        ------
        personnage : Personnage

        Returns
        -------
        Joueur
            le Joueur propriétaire du Personnage
        '''
        print("Service : trouver Joueur à partir de Personnage")
        joueur = PersonnageDao().trouver_joueur(personnage)
        print("Service : trouver Joueur à partir de Personnage - Terminé")
        return joueur

    def rejoindre_table(self, id_table, personnage):
        '''Ajouter un personnage à une table de jeu

        Parameters
        ----------
        id_table : int
            l'identifiant de la table de jeu que le personnage rejoint
        personnage : Personnage
            le personnage à ajouter

        Returns
        -------
        True si l'opération est un succés
        False sinon

          '''
        print("Service : Personnage rejoint une table")
        table = TableJeuDao().trouver_par_id(id_table)
        success = PersonnageDao().rejoindre_table(table, personnage)
        print("Service : Personnage rejoint une table - Terminé")
        return success

    def quitter_table(self, personnage, table):
        '''Le personnage quitte une table de jeu

        Parameters
        ----------
        * personnage : Personnage
            * le personnage à ajouter
        * table : TableJeu
            * la table de jeu que le personnage quitte

        Returns
        -------
        * True si l'opération est un succés
        * False sinon
        '''
        print("Service : Personnage quitte une table")
        success = PersonnageDao().quitter_table(personnage, table)
        print("Service : Personnage quitte une table - Terminé")
        return success
