INSERT INTO jdr.seance(id_seance, description, debut, fin) VALUES
(1000, 'Samedi matin',         '2022-09-24 08:00:00', '2022-09-24 13:00:00'),
(1001, 'Samedi après-midi',         '2022-09-24 14:00:00', '2022-09-24 19:00:00');


INSERT INTO jdr.table_jeu(id_table, id_seance, id_maitre_jeu, scenario, infos_complementaires) VALUES
(1000, 1000,  1000,    'Epidémie au Lazaret',                                'joueurs de niveau 5 minimum'),
(1001, 1000,  1001,    'Traversée de la Moria',                              null),
(1002, 1000,  null,    null,                                                 null),
(1003, 1000,  null,    null,                                                 null),
(1004, 1001,  1003,    'Règlement de comptes à OK corral',                   null);


INSERT INTO jdr.joueur(id_joueur, pseudo, nom, prenom, mail, est_mj) VALUES
(1000, 'mlkjhg',        'Javel',        'Aude',   'Aude.Javel@mail.fr',       true),
(1001, 'wnxbcv',        'Poree',        'Eva',    'Eva.Poree@mail.fr',        true),
(1002, 'apzoei',        'Route',        'Otto',   'Otto.Route@mail.fr',       true),
(1003, 'qpsodd',        'Bon',          'Jean',   'jeanbon@mail.fr',          true),
(1004, 'qmsldk',        'Titegoutte',        'Anne',   'Anne.Titegoutte@mail.fr',       false),
(1005, 'wqazsx',        'Titegoutte',        'Justine',   'Justine.Titegoutte@mail.fr',       false);

 
INSERT INTO jdr.personnage(id_personnage, id_joueur, nom, classe,race,niveau,competence,langues_parlees) VALUES
(1000, 1000, 'Mario',     'Fighter',   'Human',    2,   'History',         'Abyssal'),
(1001, 1001, 'Peach',     'Sorcerer',  'Human',    4,   'Deception',       'Common'),
(1002, 1002, 'Legolas',   'Ranger' ,   'Elf',      5,   'Arcana',          'Gnomish'),
(1003, 1002, 'Panoramix', 'Druid',     'Human',    0,   'Nature',          'Halfling'),
(1004, 1003, 'Gandalf',   'Wizard',    'Human',    99,  'Arcana',          'Dwarvish'),
(1005, 1003, 'Gimli',     'Fighter',   'Dwarf',    1,   'Medecine',        'Dwarvish'),
(1006, 1004, 'Gollum',     'Bard',   'Dwarf',    5,   'Nature',        'Common'),
(1007, 1005, 'Aragorn',     'Bard',   'Human',    5,   'Nature',        'Common');


INSERT INTO jdr.table_personnage(id_table, id_personnage) VALUES
(1000, 1005),
(1000, 1003),
(1000, 1007),
(1000, 1004),
(1000, 1006),
(1004, 1006),
(1004, 1002);



