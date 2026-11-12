# Aclaraciones de los manuales

## ¿Qué es esta lista?

Registra diferencias y límites encontrados en las copias analizadas. No cambia
la normativa de la organización ni decide cuál documento está vigente.

| Tema | Situación | Tratamiento en el ejercicio |
|---|---|---|
| Versiones Python | Aparecen mínimos y versiones homologadas diferentes. | Python 3.14.7 reproduce el ejercicio, sin afirmar homologación corporativa. |
| Dependencias | Conviven versiones concretas y Latest. | Se fijan versiones en cada ejemplo; no se reemplaza el catálogo interno. |
| Aprobadores | El documento general y Git Flow difieren en producción. | Se documenta el proceso sin automatizar aprobaciones ni publicar cambios. |
| Cobertura | El 75 % tiene alcances distintos y mutación es otra métrica. | Las instrucciones identifican la métrica; no se presenta un porcentaje como calidad garantizada. |
| Logs | El formatter de ejemplo no serializa algunos campos enviados con extra. | El formatter educativo selecciona y serializa order_id explícitamente. |
| MethodView | El ejemplo del manual usa métodos estáticos. | Aquí se usan métodos de instancia con self, as_view y Blueprint. |
| SQL | Hay sintaxis y reglas específicas de SQL Server. | Solo se implementa SQL de PostgreSQL; no se usa BIT ni sp_executesql. |
| Mayúsculas SQL | PostgreSQL normaliza identificadores sin comillas. | La lección de nombres muestra comillas y explica su coste. Las demás usan nombres locales en minúsculas para centrarse en SQL. |
| Asincronía | La guía de pruebas Spring excluye ciertos procesos del alcance. | Eso no significa que nunca se deban probar procesos asíncronos. |
| Timeouts | Dejar de esperar no garantiza cancelar todo el trabajo. | Se explica la cancelación cooperativa y no se promete rollback remoto. |
| Actualización dinámica | Una configuración externa no implica recarga automática. | Flags y niveles de log muestran un cambio explícito dentro del proceso. |
| OAuth0 | El término del manual es ambiguo. | Se señala para aclaración; no se implementa autenticación con un protocolo inventado. |
| Skills | Metadatos y activación dependen del runtime. | No se promete que un campo YAML tenga efectos universales ni se instala una skill. |

Los fragmentos before son contraejemplos intencionales, no recomendaciones para
copiar a producción. Los ejemplos after aíslan una práctica y declaran lo que no
resuelven; no certifican cumplimiento integral del banco.
