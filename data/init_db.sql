DROP SCHEMA IF EXISTS jdr CASCADE;
CREATE SCHEMA jdr;

-----------------------------------------------------
-- Sceance
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.sceance CASCADE ;
CREATE TABLE jdr.sceance  (
    id_sceance serial PRIMARY KEY,
    description text,
    debut timestamp,
    fin timestamp
);

-----------------------------------------------------
-- Table de jeu
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.table_jeu CASCADE ;
CREATE TABLE jdr.table_jeu  (
    id_table serial PRIMARY KEY,
    id_sceance integer,
    id_maitre_jeu integer,
    numero integer,
	scenario text
);

-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.joueur CASCADE ;
CREATE TABLE jdr.joueur(
    id_joueur serial PRIMARY KEY,
    pseudo text UNIQUE,
    nom text NOT NULL,
    prenom text NOT NULL,
    mail text
);

-----------------------------------------------------
-- Personnage
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.personnage CASCADE ;
CREATE TABLE jdr.personnage(
    id_personnage serial PRIMARY KEY,
    id_joueur integer NOT NULL,
    nom text NOT NULL,
    race text NOT NULL,
    classe text NOT NULL,
    niveau integer NOT NULL
);

-----------------------------------------------------
-- Lien entre Table et Joueur 
-- Permet de connaitre les joueurs et personnages d une table
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.table_joueur CASCADE ;
CREATE TABLE jdr.table_joueur  (
    id_table integer NOT NULL,
    id_joueur integer NOT NULL,
    id_personnage integer NOT NULL
);