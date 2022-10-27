-- Personnages par table
SELECT s.description                           "Scéance",
       to_char(debut,'DD/MM/YYYY HH24:MI')     "Début",
       to_char(fin,'DD/MM/YYYY HH24:MI')       "Fin",
       t.id_table                              "Num table",
       t.scenario                              "Scénario",
       mj.pseudo                               "Maitre du jeu",
       j.pseudo                                "Pseudo joueur",
       p.nom                                   "Personnage"
  FROM jdr.seance s 
  LEFT JOIN jdr.table_jeu t USING (id_seance)
  LEFT JOIN jdr.table_personnage tp USING(id_table)
  LEFT JOIN jdr.personnage p USING(id_personnage)
  LEFT JOIN jdr.joueur j USING (id_joueur)
  LEFT JOIN jdr.joueur mj ON t.id_maitre_jeu = mj.id_joueur;

-- Personnages par joueur
SELECT j.pseudo,
       p.*
  FROM jdr.joueur j
  LEFT JOIN jdr.personnage p USING (id_joueur);