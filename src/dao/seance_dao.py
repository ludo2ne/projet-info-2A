'''
Module joueur_dao
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from typing import List, Optional

from dao.db_connection import DBConnection
from utils.singleton import Singleton
from view.session import Session


from business_object.seance import Seance


class SeanceDao(metaclass=Singleton):
    '''
    Classe contenant les méthodes de dao de Seance
    '''

    def trouver_par_id(seld, id_seance) -> Seance:
        '''trouver une seance à partir de son id
        Params
        ------
        id_seance : int
            l'identifiant de la Seance

        Returns
        -------
        Seance : la Seance si elle a été trouvée
        '''
        print("DAO : Trouver séance par id")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "  FROM jdr.seance                      "
                        " WHERE id_seance = %(id_seance)s       ",
                        {"id_seance": id_seance})
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        seance = None
        if res:
            seance = Seance(id_seance=res["id_seance"],
                            description=res["description"],
                            debut=res["debut"],
                            fin=res["fin"])

        print("DAO : Trouver séance par id - Terminé")

        return seance

    def lister_toutes(self) -> list[Seance]:
        '''Lister toutes les Séances

        Returns
        -------
        list[Seance] : la liste de toutes les Séances
        '''
        print("DAO : Lister toutes les Séances")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "  FROM jdr.seance                      ")
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        liste_seances = []
        if res:
            for row in res:
                seance = Seance(id_seance=row["id_seance"],
                                description=row["description"],
                                debut=row["debut"],
                                fin=row["fin"])
                liste_seances.append(seance)

        print("DAO : Lister toutes les Séances - Terminé")

        return liste_seances
