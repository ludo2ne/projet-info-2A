--INSERT INTO jdr.sceance(description, debut, fin) VALUES
--('Samedi matin', '2022-09-24 08:00:00', '2022-09-24 13:00:00'),
--('Samedi après-midi', '2022-09-24 14:00:00', '2022-09-24 19:00:00'),
--('Dimanche matin', '2022-09-25 08:00:00', '2022-09-25 13:00:00'),
--('Dimanche après-midi', '2022-09-25 14:00:00', '2022-09-25 19:00:00');


INSERT INTO jdr.table_jeu(id_seance, id_maitre_jeu, scenario, infos_complementaires) VALUES
(1, 2, 'Epidémie au Lazaret', 'joueurs de niveau 5 minimum'),
(1, null, null, null),
(1, null, null, null),
(1, null, null, null);


INSERT INTO jdr.joueur(pseudo, nom, prenom, mail, est_mj) VALUES
('admin', 'admin', 'admin', 'admin@jdr.fr', false),
('pp', 'Javel', 'Aude', 'Aude.Javel@mail.fr', false),
('evabien','Poree', 'Eva', 'Eva.Poree@mail.fr', true),
('toto','Route', 'Otto', 'Otto.Route@mail.fr', false),
('calva14','Ptitegoutte', 'Anne', 'Anne.Ptitegoutte@mail.fr', false);


INSERT INTO jdr.personnage(id_joueur, nom, classe, race, niveau) VALUES
(2, 'Mario', 'Plombier', 'Humain', 2),
(2, 'Luigi', 'Magicien', 'Elfe', 1),
(3, 'Peach', 'Combattant', 'Elfe', 8),
(4, 'Daisy', 'Soigneur', 'Nain', 5);


INSERT INTO jdr.table_personnage(id_table, id_personnage) VALUES
(1, 1),
(1, 3),
(1, 4),
(2, 1),
(10001, 10001),
(10001, 10002);


INSERT INTO jdr.message(id_joueur, date_creation, contenu, lu) VALUES
(2, '2022-09-01 08:00:00', 'Vous êtes virés de la table 2', false),
(2, '2022-09-20 08:00:00', 'Vous avez été déplacé de la table 3 à la table 5', false),
(3, '2022-09-05 08:00:00', 'Bonjour', false),
(4, '2022-09-04 08:00:00', 'Bienvenu sur notre application', false);



---
--- Vue globale pour verifier que tout est ok
---

SELECT t.id_seance                                "Séance",
       t.id_table                              "Num table",
       t.scenario                              "Scénario",
       mj.pseudo                               "Maitre du jeu",
       j.pseudo                                "Pseudo joueur",
       p.nom                                   "Personnage"
  FROM jdr.table_jeu t
  LEFT JOIN jdr.table_personnage tp USING(id_table)
  LEFT JOIN jdr.personnage p USING(id_personnage)
  LEFT JOIN jdr.joueur j USING (id_joueur)
  LEFT JOIN jdr.joueur mj ON t.id_maitre_jeu = mj.id_joueur;

--SELECT s.description                           "Scéance",
--       to_char(debut,'DD/MM/YYYY HH24:MI')     "Début",
--       to_char(fin,'DD/MM/YYYY HH24:MI')       "Fin",
--       t.id_table                              "Num table",
--       t.scenario                              "Scénario",
--       mj.pseudo                               "Maitre du jeu",
--       j.pseudo                                "Pseudo joueur",
--       p.nom                                   "Personnage"
--  FROM jdr.sceance s 
--  LEFT JOIN jdr.table_jeu t USING (id_sceance)
--  LEFT JOIN jdr.table_personnage tp USING(id_table)
--  LEFT JOIN jdr.personnage p USING(id_personnage)
--  LEFT JOIN jdr.joueur j USING (id_joueur)
--  LEFT JOIN jdr.joueur mj ON t.id_maitre_jeu = mj.id_joueur;