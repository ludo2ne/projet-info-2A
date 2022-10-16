# Projet conférence de jeu de rôle

## Création du dépôt local

```bash
git clone git@github.com:ludo2ne/projet-info-2A.git
```

## Visual Studio Code 

* File > Open Folder > ==projet-info-2A==

## Packages requis

* [inquirerPy](https://inquirerpy.readthedocs.io/en/latest/)

```bash
pip install inquirerPy
pip install requests
pip install autopep8
pip install tabulate

pip list
```


## Connexion à la base de données

Informations de connexion contenues dans le fichier `.env`


## Utilisation

```bash
python src/lancement_appli.py            # pour lancer l application
python src/run_all_tests.py              # pour lancer tous les tests
```

Au tout premier lancement de l'application, choisir ==initialiser la base de données== dans le menu
**TODO** : éventuellement déplacer plus tard dans le menu Administrateur