DROP SCHEMA IF EXISTS jdr CASCADE;
CREATE SCHEMA jdr;

-----------------------------------------------------
-- Sceance
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.seance CASCADE ;
CREATE TABLE jdr.seance  (
    id_seance serial PRIMARY KEY,
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
    id_seance integer,
    id_maitre_jeu integer,
	scenario text,
    infos_complementaires text
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
    mail text,
    est_mj boolean
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
DROP TABLE IF EXISTS jdr.table_personnage CASCADE ;
CREATE TABLE jdr.table_personnage  (
    id_table integer NOT NULL,
    id_personnage integer NOT NULL
);

-----------------------------------------------------
-- Message
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.message CASCADE ;
CREATE TABLE jdr.message  (
    id_message serial PRIMARY KEY,
    id_joueur integer NOT NULL,
    date_creation timestamp,
    contenu text,
    lu boolean
);


