SELECT *,
SUM(weight) OVER() AS poids_total,
FROM furniture