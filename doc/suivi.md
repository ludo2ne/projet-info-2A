---
title: Projet info 2A
tags: Cours2A
---



:::success
* **Sujet** : Conférence de jeu de rôle
* **Tuteur / Tutrice** : Cyriel Mallart (cyrielle.mallart@gmail.com)
* [Dépôt GitHub](https://github.com/ludo2ne/projet-info-2A)
    * Git ([Présentation](https://hackmd.io/AOSXJAJiR4q7GKdbiKcKsw) - [TP initiation](https://hackmd.io/BdGZF6qOTk2qvzAlvrz_WA))
* [Dossier d'analyse](https://www.overleaf.com/7459989917xsmkkjbfvdqs)
:::


-------------------------------------------
# :dart: Échéances
-------------------------------------------

:::danger 
Rapport final :clock1: <iframe src="https://free.timeanddate.com/countdown/i83zdl7u/n1264/cf11/cm0/cu2/ct4/cs0/ca0/co0/cr0/ss0/cac009/cpcf00/pcfff/tcfff/fs100/szw256/szh108/iso2022-11-26T23:59:00" allowtransparency="true" frameborder="0" width="130" height="16"></iframe>
:::

---


```mermaid
gantt
    %% Faites bien attention a la syntaxe sinon ca va planter !
    %% doc : https://mermaid-js.github.io/mermaid/#/./gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    %% todayMarker off
    title       Diagramme de Gantt
    %% excludes  YYYY-MM-DD and/or sunday and/or weekends 

    section Livrables
    %% Voeux                        :milestone, 2022-08-28, 0d
    Dossier d'analyse            :milestone, 2022-10-08, 0d
    Rapport final                :milestone, 2022-11-26, 0d
    Soutenance                   :milestone, 2022-12-06, 0d
    
    section Rdv
    Suivi                        :milestone, 2022-08-30, 0d
    Suivi                        :milestone, 2022-09-16, 0d
    Suivi                        :milestone, 2022-09-30, 0d
    Suivi                        :milestone, 2022-10-14, 0d
    3j Immersion                 :active,    2022-10-26, 3d
    Toussaint                    :crit,      2022-10-29, 9d
    Suivi                        :milestone, 2022-11-18, 0d

    section Phases
    Organisation                 :active,      2022-08-30, 5d
    Etude                        :active,      2022-08-30, 10d
    Conception                   :active,      2022-09-05, 25d
    Rapport d'Analyse            :active,      2022-09-20, 20d
    v0 appli                     :active,      2022-09-15, 10d
    Développement                :active,      2022-10-01, 45d
    Rapport Final                :active,      2022-11-01, 20d
    Présentation                 :active,      2022-11-20, 15d
    
    
    section ToDo
    Diag Cas d'utilisation       :active,      2022-08-30, 15d
    Diag Classes                 :active,      2022-09-01, 30d
    Diag BDD                     :active,      2022-09-10, 15d
    %%Stats univariées retraités   :done,         2021-11-28, 3d
```


| Date    | Livrables                                                    |
| ------- | ------------------------------------------------------------ |
| 16 sept | ~~Avoir une v0 des différents diagrammes~~
| 08 oct. | ~~[Dossier d'analyse](https://www.overleaf.com/7459989917xsmkkjbfvdqs)~~ 
| 26 nov. | Rapport final (:hammer_and_wrench:  [correcteur orthographe et grammaire](https://www.scribens.fr/)) | 
|  6 déc. | PPT soutenance                                               |



-------------------------------------------
# :construction: Todo 
-------------------------------------------

### Organisation d'équipe

* Création des dépôts locaux et faire tourner la v0 sur chacun des postes
    * [x] Banruo, JF, Hugo
    * [ ] Décocher connexions multiples dbeaver
    * [ ] Jason

---

### Développement

* [x] [POC](https://fr.wikipedia.org/wiki/Preuve_de_concept) : faire tourner la v0.0 sur la programmation en couche [color=green][name=Ludo]
* [x] tuto pour [utiliser une BDD postgre sur son poste](https://www.youtube.com/watch?v=Cc9d2c8UuKA) [color=purple][name=Hugo]
* [ ] Se spécialiser dans certaines couches ?
* [x] Lister quelques fonctionnalités simples pour débuter [color=green][name=Ludo]
    * [ ] Fournir à chacun un dév simple
* [ ] tester [un appel à l'api](https://www.dnd5eapi.co/)
* [x] voir comment lancer tous les tests -> run_all_tests.py
* [x] script pour ré-initialiser la bdd -> utils/reset_database.py
* [ ] voir comment tester les dao sans polluer la bdd
    * avoir un schéma de données tests ?

---


### :question: Questions à la tutrice ou entre nous

* [ ] [color=green][name=Ludo] : est-ce qu'on a vraiment besoin d'un business object ==Administrateur== ?
* [color=green][name=Ludo] Points à éclairer
    * [ ] En bdd, pourquoi `seance` fait parti de la clé primaire d'une `table_jeu` ?
    * [ ] En bdd, ça me parait inévitable d'avoir une table `seance`
        * parce que dans le cas contraire dans notre appli, il n'y aura aucune info sur les horaires ni sur les demi-journées


---

* [ ] Appels à l'API
    * lors de la création, le joueur choisit la classe du Personnage
    * on récupére auprès de l'API plus d'info sur la classe
        * compétences ==proficiencies== + compétences optionnelles (choix à faire)
        * équipement ==equipment== + équipement optionnel (choix à faire)
        * caractéristiques ==features== selon le niveau, ex : "Reckless Attack"
* Est-ce que l'on doit utiliser toutes les caractèristiques des personnages fournies par l'[api](https://www.dnd5eapi.co/) ?
    * Non, à minima classe et race
* Que se passe-t-il lorsqu'un Maitre du jeu quitte la table ? Les joueurs sont virés de la table ou pas ? Non
* Distinction entre joueur et MJ ? le choix se fait à l'inscription -> ok pour la tutrice

---

* est-ce que les joueurs doivent avoir un attribut "niveau" ? Non
* est-ce que l'on peut mettre tous les attributs en public ? Petit oui
* Qui choisit le scénario d'une table, MJ ou organisateur ? MJ
* « Les organisateurs se réservent le droit ... de réorganiser les tables » : plus précisément ? Déplacer les joueurs

---



-------------------------------------------
# :robot_face: Code 
-------------------------------------------

### :arrow_forward: Utilisateur non connecté

* ==S'inscrire==
    * [x] Basculer vers la vue InscriptionVue
        * [ ] demander pseudo, nom, prenom, mail
        * [ ] JoueurService.**creer(pseudo, nom, prenom, mail)**
            * [ ] Vérifier que tous les champs remplis sont ok (non vides, mail contient @)
            * [ ] JoueurDAO.**trouver_par_pseudo()**
            * si la méthode ci-dessus ne renvoi aucun résultat
            * [x] JoueurDAO.**creer()** `INSERT INTO jdr.joueur...`
* ==Se connecter==
    * Basculer vers la vue **ConnexionVue**
        * demander pseudo
            * [x] si pseudo = Admin... 
            * sinon
                * [x] JoueurService.trouver_par_pseudo(pseudo)
                    * [x] JoueurDAO.trouver_par_pseudo(pseudo)
            * Si pseudo trouvé
                * [x] conserver pseudo en Session
                * [x] basculer vers JoueurMenuVue
* ==Quitter==

---

### :arrow_forward: JoueurMenuVue

* [color=green][name=Ludo]  [color=purple][name=Hugo]               [color=blue][name=Banruo]  [color=orange][name=Jason]  [color=red][name=JF]

---

* ==Créer un personnage== [color=purple][name=Hugo]
    * [x] Basculer vers la vue CreerPersonnageVue
        * demander infos sur le personnage (nom, classe, race, niveau)
        * [x] PersonnageService.**creer(nom, classe, race, niveau)**
            * [ ] vérifier qu'il n'a pas dejà 3 personnages
            * [ ] vérifier que classe et race existent ? faire une liste ?
            * [ ] appel API
            * [x] PersonnageDAO.**creer()**
        * [ ] test DAO
    * [ ] Test Service
* :heart: ==Supprimer un personnage== [color=red][name=JF]
    * [x] Afficher la liste des personnages
        * [x] JoueurService.**lister_personnage()**
    * [x] Basculer vers SupprimerPersonnageVue
        * demander le nom du Personnage
        * [x] Demander de confirmer la suppression
        * [ ] JoueurService.**supprimer_personnage()**
            * vérifier que le Personnage n'est pas inscrit à une table
                * [ ] PersonnageDao.**lister_tables()**
            * [x] PersonnageDao.**supprimer()**
    * [ ] :warning: si le joueur n'a aucun Personnage
* :heart: ==Lister ses personnages== [color=blue][name=Banruo]
    * [x] JoueurService.**lister_personnages()**
        * [x] récupérer le pseudo du joueur en session (pseudo = Session.pseudo)
        * [x] JoueurDao.**trouver_par_pseudo(pseudo)**
        * [x] PersonnageDao.**lister_par_joueur(Joueur)**
        * [ ] TestJoueurDao
    * [ ] TestJoueurService
* :fire: ==Rejoindre une table==
    * 1. lister les tables disponibles 
    * 2. le joueur sélectionne la table qu'il veut
    * 3. vérifier que le joueur n'est pas déjà occupé à cet horaire
    * 4. ajouter Personnage à la table
* ==Quitter une table==
    * Lister les tables ou le joueur est
        * [ ] JoueurService.voir_son_programme()
    * Basculer vers la QuitterTableVue
        * Demander le numéro de table qu'il veut quitter
        * [ ] JoueurService.**quitter_table()**
            * [ ] JoueurDao (ou PersonnageDao).**quitter_table()** 
* :heart: ==Voir son programme==
    * [ ] JoueurService.**voir_son_programme()**
        * [ ] récupérer le joueur en session : *joueur = Session().user*
        * [ ] JoueurDao.**voir_son_programme()**
        * [ ] TestJoueurDao
    * [ ] TestJoueurService
* :heart: ==Voir messages==
    * [ ] JoueurService.**voir_messages()**
        * [ ] récupérer le joueur en session : *joueur = Session().user*
        * [ ] MessageDao.**lister_par_joueur(Joueur)**
        * [ ] TestMessageDao
    * [ ] TestJoueurService
* :heart: ==Supprimer son compte== [color=red][name=JF]
    * [ ] basculer vers une vue qui pose la question : Etes vous sur ?
        * [ ] JoueurService.supprimer()
            * [ ] Récupérer le joueur en session
            * [ ] PersonnageDao.**lister_par_joueur()**
            * [ ] PersonnageDao.**quitter_table()**
            * [ ] PersonnageDao.**supprimer()**
            * [ ] JoueurDao.**supprimer(joueur)**
                * DELETE FROM jdr.joueur WHERE pseudo =
    * [ ] revenir vers AccueilVue
* :heart: ==Accéder au Menu Maître du Jeu==
    * Vérifier si le Joueur est bien MJ
        * [ ] JoueurService.est_mj()
            * [ ] JoueurDao.est_mj()
    * [ ] Basculer vers MaitreJeuMenuVue
* ==Se déconnecter== [color=green][name=Ludo]
    * [x] Supprimer le pseudo de la Session
    * [x] Basculer vers AccueilVue

---

### :arrow_forward: MaitreJeuMenuVue (:construction: à créer )


* ==Gérer une Table== [color=blue][name=Banruo]
    * [ ] Basculer vers GererTableVue
        * Demander pour quelle séance
        * Demander quel scénario et quelles infos complémentaires
        * [ ] MaitreJeuService.**gerer_table()**
            * [ ] Vérifier que le MJ est libre pour la séance
            * [ ] TableDao.**gerer_par_mj()**
                * UPDATE jdr.table SET mj = , scénario = , info_comp =
* ==Résilier une Table==
    * [ ] Lister les table ou il est MJ
    * [ ] Basculer vers ResilierTableVue
        * Demander le numero de la table
        * [ ] MaitreJeuService.**résilier_table()**
            * [ ] TableDao.resilier_mj()
* ==Voir les Tables gérées==
    * Afficher les tables ou il est MJ avec les Personnages
    * [ ] MaitreJeuService.**voir_personnages(Table)**
        * [ ] TableDao.lister_par_mj()
        * [ ] TableDao.lister_personnages()


---

### :arrow_forward: AdministrateurMenuVue

* ==Créer une Table==
    * [ ] Basculer vers la vue AdministrateurCreerTableVue
        * [ ] Demander pour quelle seance
        * [ ] AdministrateurService.**creer_table()**
            * [ ] TableJeuDao.**creer()**
* ==Supprimer une Table==
    * [ ] Lister les table vides
        * [ ] AdministrateurService.**lister_tables_vides()**
    * [ ] Basculer vers la vue AdministrateurCreerTableVue
        * Demander le numéro de table
        * [ ] AdministrateurService.**supprimer_table()**
            * [ ] TableJeuDao.**supprimer()**
* ==Supprimer un joueur==
    * [ ] Lister les joueurs
    * [ ] Basculer vers la vue SupprimerJoueurVue
        * Demander le pseudo du joueur
        * [ ] AdministrateurService.**supprimer_joueur()**
            * [ ] JoueurDao.**supprimer()**
* ==Voir le programme complet==
    * [ ] AdministrateurService.**voir_programme_complet()**
        * lister les tables et les joueurs/personnages assis
* ==Voir les messages==
    * idem que pour Joueur
* :fire: ==Déplacer un Personnage==
* :fire: ==Déplacer un Maitre du Jeu==




-------------------------------------------
# :cyclone: Base de données 
-------------------------------------------

### DBeaver

* Fenêtre > Preference
    * Formattage SQL
        * Casse des mots clefs : UPPER
        * [x] Insert spaces for tabs
    * Templates
        * sf > Modifier
            * Schéma = ==SELECT * FROM jdr.==
    * Métadonnées
        * Décocher "Ouvrir une connexion séparée pour la lecture des métadonnées"
    * Editeur SQL
        * Décocher "Ouvrir une connexion séparée pour chaque éditeur"


Pour créer une connexion vers la base de données ENSAI sur la VM : 
* cliquer sur icone ==Nouvelle connexion== en haut à gauche sous fichier
* PostgreSQL puis suivant
    * Host : sgbd-eleves.domensai.ecole
    * Port : 5432
    * Database : idxxxx
    * Nom d'utilisateur : idxxxx
    * Mot de passe : idxxxx
* cliquer sur l'icone ==SQL== 
    * coller les scripts ci-dessous (à la racine du projet)
    * à chaque fois cliquer sur la 3e icone orange ==Executer le script SQL==
        * init_db.sql
        * pop_db.sql







-------------------------------------------
# :mag_right: Dossier d'Analyse 
-------------------------------------------


### :rotating_light: Rédaction du dossier d'analyse



* [x] Regrouper tous les diagrammes de classe [color=orange][name=Jason]
    * [x] Validation 
* Introduction 
    * [x] rédaction [color=red][name=JF]
* Cahier des charges
    * [x] rédaction [color=red][name=JF]
    * [x] relecture
* Fonctionnalités
    * [x] rédaction [color=red][name=JF]
    * [x] relecture [color=green][name=Ludo]
* Organisation équipe 
    * [x] rédaction  [color=green][name=Ludo]
    * [x] relecture 
* Couche business_objet 
    * [x] rédaction [color=purple][name=Hugo]
    * [x] relecture [color=green][name=Ludo]
* Couche service 
    * [x] rédaction [color=purple][name=Hugo] 1-8
    * [x] rédaction [color=green][name=Ludo] 9-16
    * [x] relecture
* Couche vue
    * [x] rédaction [color=blue][name=Banruo]
    * [x] relecture 
* Couche DAO 
    * [x] rédaction [color=orange][name=Jason] 
    * [x] relecture 
* [x] Validation finale [color=red][name=JF] [color=green][name=Ludo]

---

### Consignes

* max 15 pages
* justifier les choix
* [Diagrammes, voir sur GitHub](https://github.com/ludo2ne/projet-info-2A/tree/main/doc/diagrammes)
    * Diag Gantt
    * Diag classe
    * Diag cas utilisation
    * Schéma de BDD


### :arrow_forward: Diagramme de classes

Le fait de programmer en couches fait que le diagramme de classes va être découpé en suivant ces mêmes couches.

Pour faire l'analogie avec un exemple un peu plus concret, imaginez le découpage en couche d'un site internet : 
* la couche Vue est uniquement de l'affichage (mise en forme) des pages web
    * il y a des boutons qui renvoient vers d'autres pages et/ou appellent des Services lorsque l'on clique dessus
* la couche Service contient le coeur des méthodes métiers
* la couche DAO permet de faire des requêtes en base de données


#### [Diagramme de classe des vues](https://github.com/ludo2ne/projet-info-2A/blob/main/doc/diagrammes/diag_classe_vues.txt)

La couche ==Vue== est la plus "proche" de l'utilisateur, ce sont elles qui permettent de faire l'interface entre l'Homme et la Machine (IHM). Les classes de cette couche vont contenir les méthodes qui sont proposées à l'utilisateur (se connecter, créer un compte, créer un personnage, rejoindre une table...)

Tout ce que font les classes Vue est : 
* afficher un menu
* lorsque l'utilisateur a effectué son choix
    * appel à des méthodes de ==Service== pour effectuer la tâche demandée
    * puis retour au menu (ou celui d'une autre classe ==Vue==)

exemple de Menus : 
```
Vue utilisateur non connecté
1. s_inscrire()
2. se_connecter()
3. quitter()

Vue joueur
1. creer_personnage()
2. rejoindre_table()
3. se_deconnecter()
...
```


#### [Diagramme de classe des services](https://github.com/ludo2ne/projet-info-2A/blob/main/doc/diagrammes/diag_classe_services.txt)

Elles vont lister tous les services proposés

#### Diagramme de classe des DAO :construction: 

Elles vont lister les méthodes permettant de lire et modifier la base de données

#### [Diagramme de classe des objets métier](https://github.com/ludo2ne/projet-info-2A/blob/main/doc/diagrammes/diag_classe_objets.txt)

Ce sont des classes avec uniquement des attributs (pas de méthode) qui représentent les objets métier dont nous avons besoin

:::info
**Exemple de cheminement entre les couches:**
* Le joueur est sur la vue ==JoueurVue==, il voit le menu des actions possibles pour un Joueur
* il choisit de sélectionner **Rejoindre une table**
    * cela appelle la méthode de service ==lister_tables_disponibles()== de la classe ==TableService==
        * cela appelle la méthode de dao ==lister_tables_disponibles()== de la classe ==TableDao== qui effectue la requête en base de données et retourne la liste de ==Table== (objet métier Table)
    * La méthode de service affiche cette liste
* le joueur saisit le numéro de la table qu'il veut rejoindre
    * si le numéro est valide
        * appel de la méthode rejoindre_table() de la classe ==JoueurService==
            * appel de la méthode ajouter_joueur_table() de la classe ==JoueurDao== qui effectue la requête d'INSERT
* affichage d'un message si ça s'est bien passé ou pas...
* le joueur est renvoyé vers la vue ==JoueurVue==
:::

### :arrow_forward: Diagramme de cas d'utilisation


:::spoiler v1
![](https://i.imgur.com/bqk3Y2B.png)
:::


:::spoiler v2
![](https://i.imgur.com/iUfl5bS.png)
:::

##### :bulb: Réflexions

* Déplacer joueur ? ie Supprimer d'une table ? + Ajouter à une table ?
* Se désister ? Quitter table
* Chosir personnage (Joueur) :arrow_right: En s'inscrivant à une table
* Joueur : :heavy_plus_sign: voir les tables sur lesquelles il est inscrit
* Voir message : à mon avis, ne pas mettre dans ce diagramme mais dans le commentaire du diagramme en disant que telle action va entrainer l'affichage d'un message au joueur




### Gantt

* Organisation
    * lister points forts de chacun, puis répartition des rôles
    * besoins de formation
    * bonne conduite : communiquer, respecter les autres, être solidaires, être force de proposition, ne pas faire en dernière minute
    * outils : 
        * suivi : hackMd, discord
        * analyse : [PlantUML](https://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000) ([features](https://plantuml.com/fr/class-diagram))
        * dev : python, DBeaver, postgre, fastApi
        * gestion de version : Git, GitHub
        * rédaction : LateX
* Etude
* Conception
* POC (Preuve de Concept)
    * coder une fonctionnalité basique
    * et vérifier que cela fonctionne bien



-------------------------------------------
# :calendar: Timeline 
-------------------------------------------

### 2022.09.30 Suivi 3

* Conseil tutrice : se spécialiser en dev (dao, service, vue)
* Créer une classe de pour garder le pseudo en session
* Mettre toutes les classes sur un seul diagramme
* Répartition de la rédaction du rapport



### 2022.09.22 Découpage diagramme de classe

* Découpage en suivant les couches

### 2022.09.20 v0.1

* Finalisation de la version 0.1 du programme
* BDD simple créée et poppée
* Vues simples crées
* Fonctionnalité "S'incscire" développée de bout en bout

### 2022.09.16 2e scéance

* Finalisation diagramme de Cas d'utilisation
* Maj diagramme classe
* Initialisation du diag de BDD


### 2022.09.15 Mise à jour diagrammes

* diagramme de Gantt
* organisation de l'équipe


### 2022.09.07 Création du projet GitHub

* il contiendra la documentation
* création d'une v0.0 du code en cours pour expliquer la programmation en couches


### 2022.09.06 Réunion d'équipe

* Diagramme de classe
* discussion des choix et des fonctionnalité
* version 2 du diagramme de cas d'utilisation


### 2022.08.30 Première scéance

les attendus du projet :
* Fiches de suivi
    * la tutrice veut simplement savoir ce qu'on a fait et où on en est
    * pas besoin de s'emmer*** avec ça, juste noter ce qu'on fait
* création d'un espace de discussion sur Discord


-------------------------------------------
# :clown_face: Rôles 
-------------------------------------------

* Chef de projet :arrow_right: Ludo
    * Suivi du projet, organisation et vérifie que chacun sait ce qu'il doit faire
* Communication avec la tutrice :arrow_right: Hugo
    * est sympa avec elle pour avoir une bonne note :wink: 
* Maître du temps :arrow_right: Banruo
    * s'assure que les délais sont bien respectés
* Rédacteur en chef :arrow_right: JF
    * validation des rapports, mise en forme, corrections
* Expert technique :arrow_right: Jason
    * Assiste les développeurs en cas de problème technique
* Développeurs :arrow_right: Tout le monde



-------------------------------------------
# :gift: Le sujet
-------------------------------------------


Une nouvelle convention de jeu de rôle arrive à Rennes ! L’activité phare de la convention sera un weekend dédié à la pratique des jeux de rôles. Plusieurs jeux se dérouleront en parallèle, chacun à une table contenant un maître/une maîtresse du jeu (MJ), ainsi que des joueurs et joueuses. Le but de ce weekend est de réunir des gens de tous horizons, de donner une première impression du jeu de rôle aux personnes n’ayant jamais essayé, mais aussi de satisfaire les joueurs plus expérimentés. Le système de jeu utilisé est Dongeons et Dragons 5E.

Les organisateurs vous sollicitent pour créer une application qui permette de gérer les tables de jeu de la conférence. Il faudra créer deux interfaces différentes : une pour les organisateurs et une pour un joueur ou MJ.

Un joueur ou une joueuse s’inscrit à la conférence en renseignant un nouveau profil. Sur ce profil, il ou elle peut déclarer des personnages différents. En utilisant l’API disponible à l’adresse https://www.dnd5eapi.co/, plus d’informations seront colléctées sur chaque personnage, et completeront sa fiche, comme les langues que le personnage parle, ses capacités physiques, etc. Une joueuse doit aussi pouvoir s’inscrire à une table, et consulter les tables auxquelles elle joue.

Les MJs ont accès à un profil similaire, où ils peuvent se porter volontaires pour plusieurs scénarios (et donc plusieurs tables). Le MJ doit aussi avoir accès à une liste des joueurs et des personnages qui seront à sa table, afin de pouvoir se préparer au mieux.

Les organisateurs se réservent le droit de supprimer des joueurs et des MJ, et de réorganiser les tables. Dans ce cas, un tel évènement sera notifié aux joueurs concernés lorsqu’ils iront consulter les tables auxquelles ils jouent.


### Fonctionnalités

* Authentification sommaire des profils organisateur/joueur/MJ
* Inscription pour un nouveau joueur ou MJ
* Complétion des fiches personnages via l’API
* Inscription/désistement à une table (avec gestion des contraintes)
* Vue du programme individuel pour chaque joueur
* Ajout/suppression des joueurs à une table
* Création/suppession de tables
* Vue générale du programme (tables, joueurs, MJs et horaires)

### Fonctionnalités avancées

* Recherche du programme d’un joueur particulier par un organisateur
* Validation des personnages par le MJ avant inscription définitive à une table
* Gestion d’un second système de jeu (Pathfinder, Call of Chtulu ou Monster of the Week, par exemple)

Aucune interface graphique n'est demandée dans ce sujet





<style>
   /* headers level 1 # */
    h1{
        color: darkblue;
        font-family: "Calibri";
        background-color: darkseagreen;
        padding-left: 10px;
    }
    h2{
        color: darkblue;        
    }
    h3{
        color: darkblue;        
    }
    h4{
        color: darkred;        
    }
</style>