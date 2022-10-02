from utils.singleton import Singleton
from business_object.joueur import Joueur


class Session(metaclass=Singleton):
    ''' Permet de stocker les données liées à une session de notre application

    Attributes
    ----------------
    user:
        Utilisateur de l'application
    '''

    def __init__(self) -> None:
        ''' Constructeur
        '''
        self.user = None
