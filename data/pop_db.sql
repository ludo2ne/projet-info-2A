INSERT INTO jdr.sceance(description, debut, fin) VALUES
('Samedi matin', '2022-09-24 08:00:00', '2022-09-24 13:00:00'),
('Samedi après-midi', '2022-09-24 14:00:00', '2022-09-24 19:00:00'),
('Dimanche matin', '2022-09-25 08:00:00', '2022-09-25 13:00:00'),
('Dimanche après-midi', '2022-09-25 14:00:00', '2022-09-25 19:00:00');


INSERT INTO jdr.table_jeu(id_sceance, id_maitre_jeu, scenario) VALUES
(1, 2, 'Epidémie au Lazaret'),
(1, null, null),
(1, null, null),
(1, null, null);


INSERT INTO jdr.joueur(pseudo, nom, prenom, mail) VALUES
('Aude45','Javel', 'Aude', 'Aude.Javel@mail.fr'),
('evabien','Poree', 'Eva', 'Eva.Poree@mail.fr'),
('toto','Route', 'Otto', 'Otto.Route@mail.fr'),
('calva14','Ptitegoutte', 'Anne', 'Anne.Ptitegoutte@mail.fr');


INSERT INTO jdr.personnage(id_joueur, nom, classe,race,niveau) VALUES
(1, 'Mario', 'Plombier','humain',2),
(2, 'Luigi', 'Magicien','poisson',1),
(3, 'Peach', 'Fee','elfe',99),
(4, 'Daisy', 'Soigneur','nain',0);


INSERT INTO jdr.table_joueur(id_table, id_joueur, id_personnage) VALUES
(1, 1, 1),
(1, 3, 3),
(1, 4, 4),
(2, 1, 1),
(10001,10001, 10001),
(10001,10002, 10002);


---
--- Vue globale pour verifier que tout est ok
---

SELECT s.description                           "Scéance",
       to_char(debut,'DD/MM/YYYY HH24:MI')     "Début",
       to_char(fin,'DD/MM/YYYY HH24:MI')       "Fin",
       t.numero                                "Num table",
       t.scenario                              "Scénario",
       mj.pseudo                               "Maitre du jeu",
       j.pseudo                                "Pseudo joueur",
       p.nom                                   "Personnage"
  FROM jdr.sceance s 
  LEFT JOIN jdr.table_jeu t USING (id_sceance)
  LEFT JOIN jdr.table_joueur tj USING(id_table)
  LEFT JOIN jdr.joueur j USING (id_joueur)
  LEFT JOIN jdr.joueur mj ON t.id_maitre_jeu = mj.id_joueur 
  LEFT JOIN jdr.personnage p ON tj.id_personnage = p.id_personnage;