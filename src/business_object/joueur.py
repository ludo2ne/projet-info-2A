'''
Module joueur
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


class Joueur:
    '''Attributes
    ----------
    pseudo : str
        pseudo du joueur
    nom : str
        nom du joueur
    prenom : str
        prenom du joueur
    id : int
        identifiant
    '''

    def __init__(self, pseudo, nom, prenom, mail, id_joueur=None, liste_personnages=[]):
        '''Constructeur de l'objet
        '''
        print("Objet : Création du joueur : " + pseudo)
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.liste_personnages = liste_personnages

    def __str__(self):
        '''Permet d'afficher les informations du joueurs
        '''
        # Dans l'affichage du joueur, seuls les noms des personnages apparaitront
        perso_list = []
        for el in self.liste_personnages:
            perso_list.append(f"{el.as_list()[1]}")
        return (f"Le joueur {self.pseudo} s'appelle {self.prenom} {self.nom}.\n" +
                f"Il a pour identifiant {self.id_joueur}\n" +
                f"Son adresse mail est {self.mail}\n" +
                f"Ses personnages sont {perso_list}")
