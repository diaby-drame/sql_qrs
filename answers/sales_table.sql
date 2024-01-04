SELECT client, SUM(montant)
FROM sales
GROUP BY client