SELECT * FROM orders
INNER JOIN details
USING (order_id)