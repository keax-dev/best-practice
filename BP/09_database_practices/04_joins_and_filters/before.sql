-- Tema: contraste educativo antes de aplicar la práctica.
BEGIN;
CREATE TEMP TABLE customer (customer_id integer PRIMARY KEY, customer_name text);
CREATE TEMP TABLE orders (order_id integer PRIMARY KEY, customer_id integer);
INSERT INTO customer (customer_id, customer_name) VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO orders (order_id, customer_id) VALUES (10, 1), (20, 2);
SELECT order_id, customer_name FROM orders CROSS JOIN customer ORDER BY order_id, customer_name;
ROLLBACK;
