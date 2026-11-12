-- Tema: contraste educativo antes de aplicar la práctica.
BEGIN;

CREATE TEMP TABLE t1 (x integer);
INSERT INTO t1 (x) VALUES (1);
SELECT x FROM t1;
ROLLBACK;
