INSERT INTO jdr.table_jeu(numero, id_demi_journee, id_maitre_jeu) VALUES
(1, 1, 2),
(2, 1, null),
(3, 1, null),
(4, 1, null);

INSERT INTO jdr.joueur(nom, prenom, mail) VALUES
('Javel', 'Aude', 'Aude.Javel@mail.fr'),
('Poree', 'Eva', 'Eva.Poree@mail.fr'),
('Route', 'Otto', 'Otto.Route@mail.fr'),
('Ptitegoutte', 'Anne', 'Anne.Ptitegoutte@mail.fr');

INSERT INTO jdr.table_joueur(id_table, id_joueur) VALUES
(1, 1),
(1, 3),
(1, 4),
(2, 1);