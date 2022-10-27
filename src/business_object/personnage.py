'''
Module personnage
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
        '''constructeur de la classe Personnage

        Parameters
        ----------
        id_personnage : int
            numéro id du personnage
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
            langues parlées par le personnage
        '''
        print("Objet : Création du personnage : " + nom)
        self.id_personnage = id_personnage
        self.nom = nom
        self.classe = classe
        self.race = race
        self.niveau = niveau
        self.competence = competence
        self.langues_parlees = langues_parlees

    def as_list(self):
        '''Renvoie les informations du Personnage

        Parameters
        ----------
        None

        Returns
        -------
        liste : list[str]
            information du personnage sous forme de liste
        Mettre les attributs sous forme de liste pour faire de l'affichage
        '''
        # TODO voir si on ajoute self.competence, self.langues_parlees
        #      impacts dans MaitreJeuService.voir_tables_gerees() et AdministrateurService.voir_programme_complet()

        liste = [self.id_personnage, self.nom,
                 self.classe, self.race, self.niveau, ]
        return liste

    def __str__(self):
        '''Renvoie les information du personnage

        Parameters
        ----------
        None

        Returns
        -------
        liste : list[str]
            information du personnage sous forme de str
        '''
        return (f"Personnage: {self.nom}: \n" +
                f" {self.race} {self.classe} de niveau {self.niveau}\n" +
                f"Compétences: {self.competence}\n" +
                f"Langues parlées: {self.langues_parlees}")
