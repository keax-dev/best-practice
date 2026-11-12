-- Tema: consultas parametrizadas.
BEGIN;
CREATE TEMP TABLE customer (customer_id integer PRIMARY KEY, customer_name text, email text);
INSERT INTO customer (customer_id, customer_name, email)
VALUES (1, 'Alice', 'alice@example.com'), (2, 'Bob', 'bob@example.com');
PREPARE find_customer(text) AS
SELECT customer_id, customer_name FROM pg_temp.customer WHERE customer_name = $1;
EXECUTE find_customer('Alice'' OR 1 = 1 --');
DEALLOCATE find_customer;
ROLLBACK;
