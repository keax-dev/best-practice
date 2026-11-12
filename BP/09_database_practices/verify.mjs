// Tema: ejecutar SQL real de PostgreSQL en memoria sin instalar un servidor.
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { PGlite } from '@electric-sql/pglite';

const root = path.dirname(fileURLToPath(import.meta.url));
const lessons = (await readdir(root, { withFileTypes: true }))
  .filter(entry => entry.isDirectory() && /^\d/.test(entry.name)).map(entry => entry.name).sort();
const outputs = new Map();
for (const lesson of lessons) {
  for (const version of ['before', 'after']) {
    const db = new PGlite();
    try {
      const sql = await readFile(path.join(root, lesson, `${version}.sql`), 'utf8');
      const results = await db.exec(sql);
      const queries = results.filter(result => result.fields.length > 0
        && !result.fields.some(field => field.name === 'QUERY PLAN'));
      outputs.set(`${lesson}/${version}`, queries.at(-1));
      console.log(`${lesson}/${version}: OK`);
    } finally {
      await db.close();
    }
  }
}
assert.equal(outputs.get('01_object_naming/after').rows[0].ID_CUSTOMER, 1);
assert.equal(outputs.get('02_parameterized_queries/before').rows.length, 2);
assert.equal(outputs.get('02_parameterized_queries/after').rows.length, 0);
assert.equal(outputs.get('03_explicit_columns/before').fields.length, 3);
assert.equal(outputs.get('03_explicit_columns/after').fields.length, 2);
assert.equal(outputs.get('04_joins_and_filters/before').rows.length, 4);
assert.equal(outputs.get('04_joins_and_filters/after').rows.length, 2);
assert.equal(outputs.get('05_constraints_and_normalization/before').rows[0].quantity, -2);
assert.deepEqual(outputs.get('05_constraints_and_normalization/after').rows, [{ order_id: 1, quantity: 2 }]);
assert.deepEqual(outputs.get('06_indexes_and_execution_plans/before').rows,
  outputs.get('06_indexes_and_execution_plans/after').rows);
assert.equal(outputs.get('06_indexes_and_execution_plans/after').rows.length, 10);
console.log('PostgreSQL: 12 scripts and behavioral checks passed.');
