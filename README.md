# Projet conférence de jeu de rôle

## Description

:construction: TODO :flag-gb: 


## Création du dépôt local

```bash
git clone git@github.com:ludo2ne/projet-info-2A.git
```

## Visual Studio Code 

* File > Open Folder > **projet-info-2A**

## Packages requis

* [inquirerPy](https://inquirerpy.readthedocs.io/en/latest/)
* requests
* psycopg2-binary
* tabulate
* autopep8
* pyfiglet
* regex
* python-dotenv

```bash
pip install -r requirements.txt
pip list
```


## Connexion à la base de données

Informations de connexion contenues dans le fichier `.env` à la racine du projet

```
HOST_WEBSERVICE=https://www.dnd5eapi.co/api

PASSWORD=idxxxx
HOST=sgbd-eleves.domensai.ecole
PORT=5432
DATABASE=idxxxx
USER=idxxx

NB_MAX_PERSONNAGES_PAR_JOUEUR=3
NB_JOUEURS_MAX_PAR_TABLE=5
NB_TABLES_MAX_PAR_SEANCE=10
```


## Utilisation

```bash
python src/main.py                       # pour lancer l application
python src/run_all_tests.py              # pour lancer tous les tests
python -m unittest
```

* Utilisez le pseudo **admin** pour vous connecter en tant qu'Administrateur
* Au tout premier lancement de l'application, choisir **initialiser la base de données** dans le menu
