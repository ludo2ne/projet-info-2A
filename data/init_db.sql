DROP SCHEMA IF EXISTS jdr CASCADE;
CREATE SCHEMA jdr;

-----------------------------------------------------
-- Table de jeu
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.table_jeu CASCADE ;
CREATE TABLE jdr.table_jeu  (
    id_table serial PRIMARY KEY,
    numero integer,
    id_demi_journee integer,
    id_maitre_jeu integer
);

-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.joueur CASCADE ;
CREATE TABLE jdr.joueur(
    id_joueur serial PRIMARY KEY,
    nom text NOT NULL,
    prenom text NOT NULL,
    mail text NOT NULL
);

-----------------------------------------------------
-- Lien entre Table et Joueur 
-- Permet de connaitre les joueurs d une table
-----------------------------------------------------
DROP TABLE IF EXISTS jdr.table_joueur CASCADE ;
CREATE TABLE jdr.table_joueur  (
    id_table integer NOT NULL,
    id_joueur integer NOT NULL
);