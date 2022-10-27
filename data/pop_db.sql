INSERT INTO jdr.seance(description, debut, fin) VALUES
('Samedi matin', '2022-09-24 08:00:00', '2022-09-24 13:00:00'),
('Samedi après-midi', '2022-09-24 14:00:00', '2022-09-24 19:00:00'),
('Dimanche matin', '2022-09-25 08:00:00', '2022-09-25 13:00:00'),
('Dimanche après-midi', '2022-09-25 14:00:00', '2022-09-25 19:00:00');


INSERT INTO jdr.table_jeu(id_seance, id_maitre_jeu, scenario, infos_complementaires) VALUES
(1, 2, 'Epidémie au Lazaret', 'joueurs de niveau 5 minimum'),
(1, 3, 'Traversée de la Moria', null),
(1, 11, 'Libérons les papillons', null),
(1, null, null, null),
(2, 2, 'Epidémie au Lazaret - le retour', 'joueurs de niveau 6 minimum'),
(2, 11, 'Il faut sauver maurice', null),
(2, null, null, null),
(3, 2, 'Epidémie au Lazaret - la revanche', null),
(3, null, null, null),
(4, 2, 'Epidémie au Lazaret - le retour de la revanche', null);


INSERT INTO jdr.joueur(pseudo, nom, prenom, mail, est_mj) VALUES
('admin',     'admin',        'admin',  'admin@jdr.fr',             false),
('pp',        'Javel',        'Aude',   'Aude.Javel@mail.fr',       true),
('evabien',   'Poree',        'Eva',    'Eva.Poree@mail.fr',        true),
('toto',      'Route',        'Otto',   'Otto.Route@mail.fr',       true),
('jj',        'Bon',          'Jean',   'jeanbon@mail.fr',          true),
('dd',        'Lapeche',      'Ella',   'ella@mail.fr',             true),
('ll',        'Masse',        'Lara ',  'l.masse@mail.fr',          false),
('oo',        'Ochon',        'Paul',   'polochon@mail.fr',         false),
('tt',        'Kiki',         'Terry',  'terry@mail.fr',            false),
('yy',        'Atrovite',     'Yves',   'atrovite@mail.fr',         false),
('tex',       'Agère',        'Tex',    'texagere@mail.fr',         true);

 
INSERT INTO jdr.personnage(id_joueur, nom, classe,race,niveau,competence,langues_parlees) VALUES
(2, 'Mario',     'Fighter',   'Human',    2,'Druid','abyssal'),
(2, 'Peach',     'Sorcerer',  'Human',    4,'Druid','abyssal'),
(3, 'Legolas',   'Ranger' ,   'Elf',      5,'Druid','abyssal'),
(3, 'Panoramix', 'Druid',     'Human',    0,'Druid','abyssal'),
(4, 'Gandalf',   'Wizard',    'Human',    99,'Druid','abyssal'),
(5, 'Gimli',     'Fighter',   'Dwarf',    1,'Druid','abyssal'),
(6, 'Luke',      'Fighter',   'Human',    10,'Druid','abyssal'),
(6, 'Leia',      'Ranger',    'Elf',      3,'Druid','abyssal'),
(7, 'Bron',      'Rogue',     'Elf',      6,'Druid','abyssal'),
(8, 'Superman',  'Warlock',   'Half-Elf', 8,'Druid','abyssal'),
(9, 'Kevin',     'Druid',     'Dwarf',    5,'Druid','abyssal');


INSERT INTO jdr.table_personnage(id_table, id_personnage) VALUES
(1, 5),
(1, 6),
(1, 7),
(2, 9),
(2, 10),
(5, 3),
(5, 5);


INSERT INTO jdr.message(id_joueur, date_creation, contenu, lu) VALUES
(2, '2022-09-01 08:00:00', 'Vous êtes virés de la table 2', false),
(2, '2022-09-20 08:00:00', 'Vous avez été déplacé de la table 3 à la table 5', false),
(3, '2022-09-05 08:00:00', 'Bonjour', false),
(4, '2022-09-04 08:00:00', 'Bienvenu sur notre application', false);



---
--- Vue globale pour verifier que tout est ok
---

-- Personnages par table
SELECT t.id_seance                             "Séance",
       t.id_table                              "Num table",
       t.scenario                              "Scénario",
       mj.pseudo                               "Maitre du jeu",
       j.pseudo                                "Pseudo joueur",
       p.nom                                   "Personnage",
       p.classe                                "Classe perso",
       p.race                                  "Race perso",
       p.niveau                                "Niveau perso"
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

SELECT j.pseudo,
       p.*
  FROM jdr.joueur j
  LEFT JOIN jdr.personnage p USING (id_joueur);