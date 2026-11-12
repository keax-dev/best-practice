-- Tema: join y filtros.
BEGIN;
CREATE TEMP TABLE customer (customer_id integer PRIMARY KEY, customer_name text);
CREATE TEMP TABLE orders (order_id integer PRIMARY KEY, customer_id integer);
INSERT INTO customer (customer_id, customer_name) VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO orders (order_id, customer_id) VALUES (10, 1), (20, 2);
SELECT o.order_id, c.customer_name
FROM pg_temp.orders AS o
INNER JOIN pg_temp.customer AS c ON c.customer_id = o.customer_id
WHERE o.order_id >= 10 ORDER BY o.order_id;
ROLLBACK;
