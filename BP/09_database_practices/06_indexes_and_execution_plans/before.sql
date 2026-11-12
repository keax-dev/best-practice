-- Tema: contraste educativo antes de aplicar la práctica.
BEGIN;
CREATE TEMP TABLE orders AS
SELECT value AS order_id, value % 1000 AS customer_id
FROM generate_series(1, 10000) AS value;
ANALYZE orders;
EXPLAIN SELECT order_id FROM orders WHERE customer_id = 42;
SELECT order_id FROM orders WHERE customer_id = 42 ORDER BY order_id;
ROLLBACK;
