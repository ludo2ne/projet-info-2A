# Role play conference project

## Description

An application to manage tables, players and game masters at a role-playing conference


## Creation of the local repository

In a git bash terminal fill the following link to clone the project:
```bash
git clone git@github.com:ludo2ne/projet-info-2A.git
```


## Visual Studio Code 

* File > Open Folder > **projet-info-2A**


## required packages to install

The packages necessary for the proper functioning of the application are :
* [inquirerPy](https://inquirerpy.readthedocs.io/en/latest/)
* requests
* psycopg2-binary
* tabulate
* autopep8
* pyfiglet
* regex

In a git bash terminal write the following instruction to install all packages which are required for the application :
```bash
pip install -r requirements.txt
pip list
```


## Create a `.env` file
Create a file called `.env` and fill in the following content in this file :

```
HOST_WEBSERVICE=https://www.dnd5eapi.co/api

PASSWORD=id1xxxx
HOST=sgbd-eleves.domensai.ecole
PORT=5432
DATABASE=idxxxx
USER=idxxx

NB_MAX_PERSONNAGES_PAR_JOUEUR=3
NB_JOUEURS_MAX_PAR_TABLE=5
NB_TABLES_MAX_PAR_SEANCE=10
NB_SEANCES_MAX=4
```


## Create a PostgreSQL database 
Create the database and fill in the following attributes in the `.env` file :
- HOST
- PASSWORD
- USER
- DATABASE
- PORT


## How to create and pop the database

You will find the following files in the **data** folder :
* `init_db.sql` to create schema and tables
* `pop_db.sql` to pop tables with a data sample

You can also use this command to call those above scripts
```bash
python src/utils/reset_database.py       # to create schema and tables and then pop tables with a data sample
```


## How to launch the app

In a git bash terminal write the following instruction to launch the app or to run all of the tests
```bash
python src/main.py                       # to launch the app
python src/run_all_tests.py              # to launch all of the tests
python -m unittest
python src/utils/reset_database.py       # to create schema and tables and then pop tables with a data sample
```


## How to log as an Administrator

use pseudo : **admin**
