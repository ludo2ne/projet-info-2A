'''
Module joueur_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''

from business_object.joueur import Joueur


class JoueurDao:
    '''
    Classe contenant les méthodes de dao de Joueur
    '''

    def creer(joueur):
        '''Creation d'un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur
        '''

        '''
        TODO requête d'insertion en bdd
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO joueur (id, nom, prenom)"\
                    " VALUES (%(joueur_sequence.nextval())s, %(nom)s, %(prenom)s,
                    {"nom": joueur.nom,
                    "prenom": joueur.prenom})
                res = cursor.fetchone()
        '''
        print("Joueur " + joueur.prenom + " " + joueur.nom + " créé en bdd")

    def lister_tous():
        '''
        Liste de tous les joueurs
        '''
        print("SELECT * FROM joueur")
