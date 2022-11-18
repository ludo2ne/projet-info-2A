-- Personnages par table
SELECT s.description                           "Scéance",
       to_char(s.debut,'DD/MM/YYYY HH24:MI')   "Début",
       to_char(s.fin,'DD/MM/YYYY HH24:MI')     "Fin",
       tj.id_table                             "Num table",
       tj.scenario                             "Scénario",
       mj.pseudo                               "Maitre du jeu",
       j.pseudo                                "Pseudo joueur",
       p.nom                                   "Personnage"
  FROM jdr.seance s 
  LEFT JOIN jdr.table_jeu tj USING (id_seance)
  LEFT JOIN jdr.table_personnage tp USING(id_table)
  LEFT JOIN jdr.personnage p USING(id_personnage)
  LEFT JOIN jdr.joueur j USING (id_joueur)
  LEFT JOIN jdr.joueur mj ON tj.id_maitre_jeu = mj.id_joueur
 ORDER BY s.id_seance,
          tj.id_table,
          j.pseudo;



-- Liste des tables avec nombres de jouers assis
WITH nb_perso_par_table AS (
SELECT id_table,
       COUNT(1) AS nb_perso
  FROM jdr.table_personnage
 GROUP BY id_table
)
SELECT s.description             "Séance",
       tj.id_table               "Numéro Table",
       mj.pseudo                 "Maitre du Jeu",
       tj.scenario               "Scénario",
       tj.infos_complementaires  "Infos complémentaires",
       nppt.nb_perso             "Nb joueurs assis"
  FROM jdr.table_jeu tj 
 INNER JOIN jdr.seance s USING(id_seance)
 INNER JOIN nb_perso_par_table nppt USING(id_table)
  LEFT JOIN jdr.joueur mj ON mj.id_joueur = tj.id_maitre_jeu
 ORDER BY s.id_seance,
          tj.id_table;


-- Personnages par joueur
SELECT j.pseudo,
       p.*
  FROM jdr.joueur j
  LEFT JOIN jdr.personnage p USING (id_joueur);


-- Infos joueurs
WITH nb_perso AS (
SELECT id_joueur,
       COUNT(1) nb_perso
  FROM jdr.personnage p
 GROUP BY p.id_joueur 
),
nb_table_as_mj AS (
SELECT id_maitre_jeu,
       COUNT(1) nb_table_mj
  FROM jdr.table_jeu tj
 GROUP BY tj.id_maitre_jeu 
),
nb_table_as_joueur AS (
SELECT p.id_joueur,
       COUNT(1) nb_table_j
  FROM jdr.table_personnage tp
 INNER JOIN jdr.personnage p USING(id_personnage)
 GROUP BY p.id_joueur 
)
SELECT j.est_mj,
       j.pseudo,
       J.nom,
       j.prenom,     
       COALESCE(nb.nb_perso,0)     "Nb personnages",
       COALESCE(ntam.nb_table_mj,0) "Nb tables as MJ" ,
       COALESCE(ntaj.nb_table_j,0) "Nb tables as Joueur"      
  FROM jdr.joueur j
  LEFT JOIN nb_perso nb USING(id_joueur)
  LEFT JOIN nb_table_as_mj ntam ON ntam.id_maitre_jeu = j.id_joueur
  LEFT JOIN nb_table_as_joueur ntaj USING(id_joueur)
 WHERE pseudo != 'admin'
 ORDER BY j.est_mj,
          j.pseudo;