-- Joueurs par table
SELECT t.numero "num table",
       j.prenom,
       j.nom
  FROM jdr.joueur j 
 INNER JOIN jdr.table_joueur tj USING (id_joueur)
 INNER JOIN jdr.table_jeu t USING (id_table)