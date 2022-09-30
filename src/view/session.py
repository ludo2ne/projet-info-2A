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

    def home_menu(self):
        ''' Méthode d'instance home_menu
            Permet de revenir au menu principal selon le type d'utilisateur
            en vérifiant qu'il est bien connecté
        '''
        if not self.user:
            from view.accueil_vue import AccueilVue
            return AccueilVue()
        else:
            if isinstance(self.user, Joueur):
                from view.joueur_menu_vue import JoueurMenuVue
                return SuperviseurView()
            else:
                from view.agent.agent_view import AgentView
                return AgentView()
