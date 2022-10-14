'''
Module reset_database
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''


from utils.singleton import Singleton
from dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    '''
    Reinitialisation de la base de données
    '''

    def lancer(self):
        print("Réinitialisation de la base de données")

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        pop_db = open("data/pop_db.sql", encoding="utf-8")
        pop_db_as_string = pop_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)
        except Exception as e:
            print(e)
            raise

        return True


if __name__ == '__main__':
    ResetDatabase().lancer()
