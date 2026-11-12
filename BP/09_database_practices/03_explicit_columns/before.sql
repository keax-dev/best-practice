-- Tema: contraste educativo antes de aplicar la práctica.
BEGIN;
CREATE TEMP TABLE customer (customer_id integer PRIMARY KEY, customer_name text, email text);
INSERT INTO customer (customer_id, customer_name, email)
VALUES (1, 'Alice', 'alice@example.com'), (2, 'Bob', 'bob@example.com');
SELECT * FROM customer ORDER BY customer_id;
ROLLBACK;
