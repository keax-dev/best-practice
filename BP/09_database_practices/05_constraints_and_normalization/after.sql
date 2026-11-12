-- Tema: restricciones y normalización.
BEGIN;

CREATE TEMP TABLE customer (customer_id integer PRIMARY KEY, customer_name text NOT NULL);
CREATE TEMP TABLE orders (
    order_id integer PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES customer(customer_id),
    quantity integer NOT NULL CHECK (quantity > 0)
);
INSERT INTO customer (customer_id, customer_name) VALUES (1, 'Alice');
INSERT INTO orders (order_id, customer_id, quantity) VALUES (1, 1, 2);
DO $$
BEGIN
    BEGIN
        INSERT INTO orders (order_id, customer_id, quantity) VALUES (2, 1, -2);
        RAISE EXCEPTION 'Expected quantity check to reject this row';
    EXCEPTION WHEN check_violation THEN
        NULL;
    END;
END $$;
SELECT order_id, quantity FROM pg_temp.orders ORDER BY order_id;
ROLLBACK;
