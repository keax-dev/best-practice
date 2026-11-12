-- Tema: contraste educativo antes de aplicar la práctica.
BEGIN;

CREATE TEMP TABLE order_flat (order_id integer, customer_name text, quantity integer);
INSERT INTO order_flat (order_id, customer_name, quantity) VALUES (1, 'Alice', -2);
SELECT order_id, quantity FROM order_flat;
ROLLBACK;
