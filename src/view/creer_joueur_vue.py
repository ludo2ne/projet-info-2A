from InquirerPy import prompt
from service.joueur_service import JoueurService


class CreerJoueurVue():
    def __init__(self, ):
        self.questions = [
            {
                "type": "input",
                "name": "nom",
                "message": "Entrez le nom de l'utilisateur :"
            },
            {
                "type": "input",
                "name": "prenom",
                "message": "Entrez le prénom de l'utilisateur :"
            }
        ]

    def clear_console(self) -> None:
        for i in range(0, 20):
            print("")

    def display_header(self):
        self.clear_console()

    def make_choice(self):

        answers = prompt(self.questions)

        # On appelle le service de creation de joueur
        joueur = JoueurService().creer(
            answers["nom"], answers["prenom"])

        # On récupère le mesage à afficher (succès ou échec)
        if not joueur:
            print("La création du joueur a échoué")
        else:
            print("Le joueur {} {} a bien été créé".format(
                joueur.prenom, joueur.nom))

        from view.accueil_vue import AccueilVue
        return AccueilVue()
