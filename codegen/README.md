# Generación API first para todo el ejercicio

Los cuatro `contracts/openapi.yaml` son la referencia de sus APIs. Se utiliza
OpenAPI Generator **7.27.0**, generador `python-flask`, con plantillas Mustache
compartidas. La aplicación ejecuta Flask y `MethodView`, sin Connexion.

## Preparación y comandos

Desde la raíz, con Python 3.14.7 y Java 21 en `PATH`:

```powershell
java -version
.\.venv\Scripts\python.exe -m pip install -r .\requirements-codegen.txt
.\.venv\Scripts\python.exe scripts\generate_apis.py
.\.venv\Scripts\python.exe scripts\generate_apis.py --check
```

Por aplicación:

```powershell
.\.venv\Scripts\python.exe scripts\generate_apis.py --app auth
.\.venv\Scripts\python.exe scripts\generate_apis.py --app orders
.\.venv\Scripts\python.exe scripts\generate_apis.py --app inventories
.\.venv\Scripts\python.exe scripts\generate_apis.py --app gateway
```

Añade `--check` para comprobar sin escribir. Java y las herramientas de generación
se necesitan al regenerar y ejecutar las pruebas de generación; arrancar Flask
con los artefactos versionados requiere solo las dependencias de ejecución.
El antiguo `scripts/generate_auth.py` delega al generador común seleccionando Auth.

## Archivos que se generan

En `api/generated/` de cada aplicación:

- `models/`: dataclasses inmutables y esquemas Marshmallow para cada schema del contrato.
- `interfaces/`: API abstracta con métodos derivados de los `operationId`.
- `routes.py`: `Blueprint`, vistas `MethodView`, parámetros, deserialización,
  serialización y registro mediante `as_view()` y `add_url_rule()`.
- `runtime.py`: soporte de serialización y validación de fechas UTC.
- `manifest.json`: versión del generador, aplicación, huella de entradas y lista de archivos.

Los nombres y restricciones proceden de los contratos. El script añade metadatos
de generación a una copia temporal del OpenAPI para representar tipos Python,
validadores y parámetros. No mantiene una segunda lista manual de campos o rutas.
Cada aplicación conserva `codegen/config.yaml`, que configura su paquete, interfaz
y clientes. Las plantillas compartidas se encuentran en `codegen/templates/`.

Las construcciones cubiertas son las que utiliza este ejercicio: operaciones
GET/POST sin tags, parámetros obligatorios de ruta/header/query, cuerpos JSON
obligatorios de DTO, una respuesta exitosa de DTO o lista de DTO, objetos cerrados
con propiedades obligatorias, strings, enteros, booleanos, diccionarios libres,
UUID, fechas UTC, nulos, enums, patrones y restricciones de longitud/rango.
Antes de utilizar construcciones adicionales hay que ampliar las plantillas y
sus pruebas; el comando rechaza las que no soporta en vez de ignorar restricciones.

## Qué implementamos manualmente

Las clases `AuthAPIImpl`, `OrdersAPIImpl`, `InventoryAPIImpl` y `GatewayAPIImpl`
heredan de su interfaz generada. Adaptan los DTO a los servicios y modelos de
negocio. Las clases abstractas impiden instanciar una implementación que omita
métodos requeridos; las firmas tipadas documentan sus parámetros y respuestas.

Los repositorios, la lógica de pedidos, locks/idempotencia, usuarios, emisión de
JWT y permisos siguen siendo manuales. El gateway verifica JWT y roles antes de
que las rutas generadas invoquen la implementación. Los servicios comprueban la
clave interna y la propiedad de los pedidos. No se confía en identidad enviada
libremente por el usuario.

El gateway devuelve un `flask.Response` del transporte para conservar cuerpo,
código y encabezados del destino. La ruta generada reconoce ese resultado y no lo
vuelve a serializar. `ContractView` valida después su conformidad; una respuesta
inválida del destino sigue devolviendo 502.

## Cliente generado de descuentos

La configuración de Pedidos selecciona `deductInventory` del contrato del gateway.
Se generan transporte y DTO en `api/generated/clients/inventory/`.
`api/clients/inventory.py` consume ese cliente, interpreta la respuesta de negocio
y actualiza el estado a través del servicio de Pedidos.

El cliente recibe `API_GATEWAY_URL`, los timeouts y `X-Orders-Service-Key` al
construirse. No llama directamente al puerto de Inventario, no importa el código
de otro servicio y no añade reintentos. Su ruta y serialización vienen del contrato
público del gateway, que admite esa credencial interna para descuentos.

## Flujo de trabajo

1. Cambia el contrato y sus ejemplos. Si cambia una operación publicada, mantén
   alineados gateway y servicio.
2. Ejecuta `scripts/generate_apis.py` para regenerar todas las APIs y dependencias.
3. Adapta la implementación manual y los mapeos que lo necesiten.
4. Ejecuta `scripts/generate_apis.py --check`.
5. Detén los servidores manuales y ejecuta `scripts/verify.py`.
6. Revisa y versiona contratos, configuración, plantillas, artefactos e implementación.

No edites `api/generated/` a mano. Las pruebas detectan diferencias con una nueva
generación, verifican entradas/salidas tipadas y comprueban regeneración sin perder
la implementación. Las diferencias de fin de línea LF/CRLF no producen cambios falsos.

El generador trabaja primero en un directorio temporal. Solo publica dentro del
`api/generated/` seleccionado; no sobrescribe configuración local, secretos,
servicios, repositorios ni implementaciones manuales. Para pruebas de evolución
puedes usar `--contract` y `--output`, seleccionando una sola `--app` y un directorio
de salida de pruebas. `--check` no modifica los artefactos comparados.

Reinicia las aplicaciones después de regenerar: no hay recargador automático.
