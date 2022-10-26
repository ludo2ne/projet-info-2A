'''
Module supprimer_personnage_vue
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 26/10/2022
Licence : Domaine public
Version : 1.0
'''
from InquirerPy import prompt
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService
from view.session import Session
from business_object.joueur import Joueur


class GererTableVue(VueAbstraite):

    def __init__(self, message=""):
        joueur = Session().user

        self.questions = [
            {   # demander le séance a rejoindre
                "type": "list",
                "name": "seance",
                "message": "Sélectionner la séance à laquelle vous souhaitez participer",
                "choices": ["1. samedi matin",
                            "2. samedi après-midi",
                            "3. dimanche matin",
                            "4. dimanche après-midi"]},
            {   # demander le scenario
                "type": "input",
                "name": "scenario",
                "message": "Indiquez le scénario que vous voulez diriger :"},
            {   # demander l'information complementaire
                "type": "input",
                "name": "info_comple",
                "message": "Si vous souhaitez ajouter quelque chose, écrivez ici."
            }
        ]
        self.message = message

    def afficher(self):
        self.nettoyer_console()  # laisser suffisamment d'espace avec la vue precedente
        print(self.message)
        print()  # nous laisse un espace

    def choisir_menu(self):
        mj = Session().user
        # recuperer les reponses saisies par le maitre de jeu
        reponse = prompt(self.questions)
        seance = int(reponse["seance"][0])
        scenario = reponse["scenario"]
        info_comple = reponse["info_comple"]

        # verifier que si MJ est libre pour la sceance
        if MaitreJeuService().dispo_mj == False:
            message = "Vous ne pouvez pas jouer à tables en même temps, veuillez vérifier pour quelle table vous vous êtes inscrit et la séance correspondant"
            from view.maitre_jeu_menu_vue import MaitreJeuMenuVue
            return MaitreJeuMenuVue(message)


# en-dessus a verifier, ceux pour maitrejeusevice.gerertable()...... a faire

        # La suppression est annulée en l'absence de confirmation
        if not confirm:
            message = "Suppression du compte annulée"
            from view.joueur_menu_vue import JoueurMenuVue
            prochainevue = JoueurMenuVue(message)
        else:
            # On appelle le service de suppression de compte
            statut_suppression = JoueurService().supprimer(joueur)
            # On récupère le message à afficher (succès ou échec)
            if not statut_suppression[0]:
                #                message = "La suppression du compte a échoué"
                from view.joueur_menu_vue import JoueurMenuVue
#                prochainevue = JoueurMenuVue(message)
                prochainevue = JoueurMenuVue(statut_suppression[1])
            else:
                message = f"Votre compte a bien été supprimé. Au revoir {joueur.prenom}"
                Session().user = None
                from view.accueil_vue import AccueilVue
                prochainevue = AccueilVue(message)
        return prochainevue
