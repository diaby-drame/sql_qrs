SELECT year, region, SUM(population) FROM population
GROUP BY
GROUPING SETS ((year,region),year) ORDER BY year