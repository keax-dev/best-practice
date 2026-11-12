-- Tema: índices y planes de ejecución.
BEGIN;
CREATE TEMP TABLE orders AS
SELECT value AS order_id, value % 1000 AS customer_id
FROM generate_series(1, 10000) AS value;
ANALYZE orders;
CREATE INDEX idx_orders_customer_id ON orders (customer_id);
ANALYZE orders;
EXPLAIN SELECT order_id FROM orders WHERE customer_id = 42;
SELECT order_id FROM orders WHERE customer_id = 42 ORDER BY order_id;
ROLLBACK;
