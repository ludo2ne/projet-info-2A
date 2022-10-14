'''
Module joueur_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


from business_object.joueur import Joueur
from business_object.personnage import Personnage
from dao.joueur_dao import JoueurDao
from dao.table_jeu_dao import TableJeuDao
from view.session import Session


class JoueurService:
    '''
    Classe contenant les méthodes de service de Joueur
    '''

    def creer(self, pseudo, nom, prenom, mail):
        '''Service de création d'un joueur

        Parameters
        ----------
        pseudo : str
            pseudo du joueur
        nom : str
            nom du joueur
        prenom : str
            prenom du joueur
        mail : str
            mail du joueur

        Returns
        -------
        Joueur : le joueur créé
        '''
        print("Service de création de joueur")

        joueur_dao = JoueurDao()

        nouveau_joueur = Joueur(pseudo, nom, prenom, mail)
        joueur_dao.creer(nouveau_joueur)

        return nouveau_joueur

    def rejoindre_table(self, table, joueur, personnage) -> bool:
        '''Rejoindre une table s'il y a de la place

        Parameters
        ----------
        table : Table
            la table sur laquelle on ajoute le joueur
        joueur : Joueur
            Joueur à ajouter
        personnage : Personnage
            Personnage choisi par le joueur
        '''
        success = False

        # TODO verifier que le joueur est libre a cet horaire

        # y a t il encore de la place a la table
        nb_joueurs_table = TableJeuDao().get_nb_joueurs(table)

        if nb_joueurs_table <= table.nb_joueurs_max:
            success = joueur_dao.ajouter_joueur(table, joueur, personnage)
        else:
            print("Impossible d'ajouter de nouveaux joueurs à la table")
            print("Nombre de joueurs maximum : " + table.nb_joueurs_max)
            print("Nombre de joueurs actuellement : " + nombre_actuel_joueurs)

        return success

    def lister_tous(self):
        '''Service pour lister tous les joueurs

        Returns
        -------
        liste[Joueur]
        '''
        return JoueurDao().lister_tous()

    def trouver_par_pseudo(self, pseudo):
        '''Trouver un joueur à partir de son pseudo

        Returns
        -------
        Joueur
        '''
        print("INFO : JoueurService.trouver_par_pseudo({})".format(pseudo))
        return JoueurDao().trouver_par_pseudo(pseudo)

    def creer_personnage(self, nom, classe2, race, niveau):
        '''
        '''
        print("INFO : Service de création de personnage")

        perso = Personnage(id_personnage=None,
                           nom=nom,
                           classe=classe2,
                           race=race,
                           niveau=niveau)

        created = JoueurDao().creer_personnage(perso)

        print(created)

        return perso

    def lister_personnages(self):
        '''Lister les personnages d'une utilisateur

        Returns
        -------
        '''
        joueur = Session().user

        personnages = JoueurDao().lister_personnages(joueur)
        resultat = ""
        for i in personnages:
            resultat += i.nom + " " + i.classe + "\n"
        return resultat
