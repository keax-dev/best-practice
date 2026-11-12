-- Tema: contraste educativo antes de aplicar la práctica.
BEGIN;
CREATE TEMP TABLE customer (customer_id integer PRIMARY KEY, customer_name text, email text);
INSERT INTO customer (customer_id, customer_name, email)
VALUES (1, 'Alice', 'alice@example.com'), (2, 'Bob', 'bob@example.com');
SELECT customer_id, customer_name FROM customer WHERE customer_name = 'Alice' OR 1 = 1;
ROLLBACK;
