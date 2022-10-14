'''
Module joueur
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 06/09/2022
Licence : Domaine public
Version : 1.0
'''


class Personnage:
    '''Attributes
    ----------
    id_personnage : int
        id du personnage
    nom : str
        nom du personnage
    classe : str
        classe du personnage
    race : str
        race du personnage
    niveau : int
        niveau du personnage
    competence : list[str]
        liste des competence du personnage
    langues_parlees : list[str]
        liste des langues parlés par le personnage
    '''

    def __init__(self, id_personnage, nom, classe, race, niveau, competence=None, langues_parlees=None):
        print("Objet : Création du personnage : " + nom)
        self.id_personnage = id_personnage
        self.nom = nom
        self.classe = classe
        self.race = race
        self.niveau = niveau
        self.competence = competence
        self.langues_parlees = langues_parlees
