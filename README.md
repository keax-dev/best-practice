# Pedidos, Inventario y API Gateway con Flask

Ejercicio educativo de componentes backend con **OpenAPI 3.0.3 y contract-first**.
Probado con **Python 3.14.7**. Rama: `types_backend_components`.

## Guía paso a paso: desde cero hasta el primer pedido

Sigue estos pasos en orden. Los comandos usan PowerShell y no necesitan activar
el entorno virtual. No necesitas PostgreSQL, un gestor de base de datos, Docker
ni ejecutar migraciones.

### 1. Comprobar los requisitos

Necesitas Windows con PowerShell, Git y Python 3.14.7. Para instalar las
dependencias por primera vez necesitas conexión a Internet.

```powershell
git --version
py -3.14 --version
```

El segundo comando debe mostrar `Python 3.14.7` para reproducir exactamente el
entorno verificado. Si `py` no existe, instala Python con su lanzador para Windows
y abre una terminal nueva. No copies una carpeta `.venv` de otra computadora:
créala en esa máquina usando su instalación de Python.

### 2. Obtener el código y seleccionar la rama

En una computadora donde todavía no tengas el repositorio:

```powershell
cd "$env:USERPROFILE\Documents"
git clone --branch types_backend_components https://github.com/keax-dev/coe-ing.git
cd .\coe-ing
```

Si ya tienes este repositorio, entra en él y comprueba primero sus cambios:

```powershell
cd C:\Users\jimen\Documents\coe-ing
git status
git switch types_backend_components
git pull --ff-only origin types_backend_components
```

Si Git indica que hay cambios locales que impiden cambiar de rama o actualizar,
consérvalos y resuelve esa situación antes de continuar; no uses comandos de
descarte. En otra computadora sustituye la ruta por la de tu copia del repositorio.
Los siguientes comandos se ejecutan desde la carpeta raíz `coe-ing`.

### 3. Crear el entorno e instalar todas las dependencias

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r .\api-gateway\requirements.txt -r .\onb-msa-sp-orders\requirements.txt -r .\onb-msa-sp-inventories\requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Si ya tienes `.venv` con Python 3.14.7, omite su creación y ejecuta la instalación
y la comprobación. El resultado esperado de `pip check` es
`No broken requirements found.`. `pytest` se instala con esos mismos archivos.
La instalación se hace una vez; repítela cuando cambien las dependencias.

### 4. Preparar la configuración local

Los valores predeterminados permiten ejecutar todo sin configurar nada. Si quieres
tener archivos editables, créalos solamente cuando no existan:

```powershell
if (-not (Test-Path .\api-gateway\.env)) {
    Copy-Item .\api-gateway\.env.example .\api-gateway\.env
}
if (-not (Test-Path .\onb-msa-sp-orders\.env)) {
    Copy-Item .\onb-msa-sp-orders\.env.example .\onb-msa-sp-orders\.env
}
```

Inventario no requiere variables de entorno. Los `.env` son locales y están
excluidos de Git. La tabla de configuración más abajo explica todos los valores.

### 5. Ejecutar la verificación completa antes de arrancar manualmente

Deja libres los puertos 5000, 5001 y 5002 y ejecuta:

```powershell
.\.venv\Scripts\python.exe scripts\verify.py
```

Resultado verificado: **67 pruebas aprobadas** distribuidas en gateway (14),
pedidos (28), inventario (19) y contratos/recorrido HTTP completo (6).
La prueba global inicia y detiene sus propios servidores; cuando termina no deja
las aplicaciones levantadas. Si falla, revisa el mensaje antes de continuar.

### 6. Levantar las tres aplicaciones

Abre **tres terminales de PowerShell distintas**. En cada una entra primero en la
raíz de tu repositorio. En esta computadora la ruta es
`C:\Users\jimen\Documents\coe-ing`.

Terminal 1:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\onb-msa-sp-inventories\app.py
```

Terminal 2:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\onb-msa-sp-orders\app.py
```

Terminal 3:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\api-gateway\app.py
```

Mantén esas terminales abiertas. Cada comando ocupa su terminal hasta detenerlo.
Debes ver `Running on http://127.0.0.1:5002`, `:5001` y `:5000`, respectivamente.
El aviso de Flask sobre el servidor de desarrollo es normal para esta práctica.

### 7. Comprobar salud, documentación y el recorrido completo

Abre una **cuarta terminal**, que usarás como cliente:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
Invoke-RestMethod http://127.0.0.1:5001/health
Invoke-RestMethod http://127.0.0.1:5002/health

$baseUrl = "http://127.0.0.1:5000"
Invoke-RestMethod "$baseUrl/api/v1/inventories"
$order = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -ContentType "application/json" -Body '{"product_id":1,"quantity":2}'
$order | Format-List
Invoke-RestMethod "$baseUrl/api/v1/orders/$($order.id)"
Invoke-RestMethod "$baseUrl/api/v1/inventories/1"
```

Cada health debe devolver `status: ok`. Con Inventario recién iniciado, el pedido
debe quedar `CONFIRMADO`, con `reason` nulo, y el café debe quedar con stock 8.
La creación devuelve HTTP 201; `Invoke-RestMethod` muestra directamente su cuerpo.
Si repites la creación generarás otro pedido y consumirás otras dos unidades.

Abre http://127.0.0.1:5000/docs en el navegador para probar las operaciones desde
Swagger UI. Los enlaces de las tres aplicaciones aparecen en la tabla de documentación.
Las solicitudes de negocio del cliente deben apuntar al puerto 5000.

### 8. Detener, reiniciar y volver a trabajar otro día

Pulsa `Ctrl+C` en la terminal de cada aplicación; puedes detener primero gateway,
después pedidos y finalmente inventario. Para reiniciar el ejercicio desde cero,
detén ambos servicios y vuelve a ejecutar los tres comandos del paso 6.

Reiniciar únicamente Pedidos borra sus pedidos; reiniciar únicamente Inventario
restablece stock e idempotencia, sin borrar los pedidos que conserva el otro proceso.
Para un estado inicial coherente, reinicia ambos servicios.

La próxima vez no necesitas volver a crear `.venv`: entra en el repositorio,
instala dependencias si cambiaron y repite los pasos 6 y 7. Después de suspender
Windows, comprueba los tres health al reanudar; si cerraste las terminales, vuelve
a arrancar las aplicaciones. No hay servicios instalados que arranquen automáticamente.

## Solución de problemas al levantar el ejercicio

| Problema | Qué revisar |
|---|---|
| `py` no se reconoce | Instala Python con su lanzador y abre una nueva terminal. |
| No existe `.venv\Scripts\python.exe` | Entra en la raíz y crea el entorno con el paso 3. |
| `ModuleNotFoundError` | Usa el Python de `.venv` e instala los tres `requirements.txt`. |
| No se encuentra `app.py` | Usa las rutas completas desde la raíz indicadas en el paso 6. |
| Puerto ocupado o error de enlace | Detén la instancia anterior con `Ctrl+C`; no ejecutes dos copias de la misma app. |
| El navegador no conecta | Comprueba la terminal de esa app, su puerto y su `/health`. |
| Gateway responde 502 o 504 | Comprueba que el servicio destino está levantado y que las URLs y timeouts coinciden. |
| Pedido queda `ERROR_VALIDACION` | Revisa gateway e inventario y los logs de sus terminales. No implica stock insuficiente. |
| Swagger UI se ve vacío | Comprueba Internet para cargar los recursos del CDN y abre `/openapi.yaml`. |
| Las pruebas dicen que un puerto está ocupado | Detén las tres apps manuales antes de ejecutar `scripts/verify.py`. |
| Ya no quedan las existencias iniciales | Reinicia ambos servicios para comenzar una práctica nueva. |

Para identificar quién escucha en los puertos del ejercicio, sin cerrar procesos:

```powershell
Get-NetTCPConnection -LocalPort 5000,5001,5002 -State Listen -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

Los logs aparecen en las terminales de las aplicaciones. No necesitas abrir una
base de datos, cargar archivos de datos ni ejecutar comandos adicionales de infraestructura.

## Objetivo y arquitectura

Crear pedidos de un solo producto, almacenarlos en memoria y validar su
disponibilidad descontando unidades de Inventario. Toda comunicación entre
aplicaciones usa HTTP, incluyendo la llamada de Pedidos hacia Inventario.

```text
Cliente → API Gateway :5000 → Pedidos :5001
                ↑                 │ guarda CREADO
                │                 │ solicita descuento HTTP
                └─────────────────┘
                │
                └──────────→ Inventario :5002
                                  │ valida y descuenta con lock
                ←─────────────────┘
                │ devuelve resultado a Pedidos
                └──→ Pedidos actualiza estado → Gateway → Cliente
```

Recorrido obligatorio: **Cliente → API Gateway → Pedidos → API Gateway → Inventario**.

| Aplicación | Responsabilidad | Puerto |
|---|---|---|
| `api-gateway` | Validar y reenviar las operaciones permitidas | 5000 |
| `onb-msa-sp-orders` | Guardar pedidos y coordinar su validación síncrona | 5001 |
| `onb-msa-sp-inventories` | Mantener productos y descontar stock atómicamente | 5002 |

El gateway no guarda datos de negocio. Cada servicio tiene su propia memoria;
no comparte diccionarios ni importa almacenamiento de otra aplicación.

## Estructura

```text
api-gateway/
  contracts/openapi.yaml
  api/
    __init__.py                 # create_app()
    contract.py                 # MethodView + OpenAPI + documentación
    errors.py
    routes/proxy.py             # Blueprint, as_view(), add_url_rule()
    clients/proxy.py             # transporte HTTP con requests
  test/
    conftest.py
    routes/test_proxy.py
    test_contract.py
  app.py
  config.py
  requirements.txt
  .env.example
  .gitignore
onb-msa-sp-orders/
  contracts/openapi.yaml
  api/
    __init__.py
    contract.py
    errors.py
    models/order.py
    schema/order.py
    routes/order.py
    services/order.py
    repositories/order.py
    clients/inventory.py        # solo conoce API_GATEWAY_URL
  test/
    conftest.py
    routes/test_orders.py
    test_contract.py
  app.py
  config.py
  requirements.txt
  .env.example
  .gitignore
onb-msa-sp-inventories/
  contracts/openapi.yaml
  api/
    __init__.py
    contract.py
    errors.py
    seed.py
    models/product.py
    schema/inventory.py
    routes/inventory.py
    services/inventory.py
    repositories/inventory.py
  test/
    conftest.py
    routes/test_inventory.py
    test_contract.py
  app.py
  config.py
  requirements.txt
  .env.example
  .gitignore
test/
  test_contracts.py             # validación y compatibilidad de contratos
  test_system.py                # tres procesos reales y fallos HTTP
scripts/verify.py               # suites en procesos separados
README.md
```

Los paquetes contienen sus `__init__.py`. Las carpetas con guiones son proyectos
independientes, no paquetes importables. Cada aplicación incluye su pequeña
integración OpenAPI para poder ejecutarse sola.

## Instalación en PowerShell

Desde la raíz, con Python 3.14 instalado:

```powershell
cd C:\Users\jimen\Documents\coe-ing
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r .\api-gateway\requirements.txt -r .\onb-msa-sp-orders\requirements.txt -r .\onb-msa-sp-inventories\requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Si `.venv` ya existe y utiliza Python 3.14.7, reutilízalo. No hace falta activar
el entorno ni cambiar la política de PowerShell. Las dependencias directas tienen
versiones fijadas. Las aplicaciones pueden compartir el entorno virtual y siguen
siendo procesos independientes. También puedes instalar cada `requirements.txt`
en un entorno propio si ejecutas las aplicaciones por separado.

Opcionalmente copia las configuraciones de ejemplo; los valores predeterminados
ya permiten ejecutar sin `.env`:

```powershell
Copy-Item .\api-gateway\.env.example .\api-gateway\.env
Copy-Item .\onb-msa-sp-orders\.env.example .\onb-msa-sp-orders\.env
```

No sobrescribas un `.env` personalizado. Las variables del entorno tienen prioridad.

## Ejecución en tres terminales

En cada terminal parte desde `C:\Users\jimen\Documents\coe-ing`.

Terminal 1, Inventario:

```powershell
cd .\onb-msa-sp-inventories
..\.venv\Scripts\python.exe app.py
```

Terminal 2, Pedidos:

```powershell
cd .\onb-msa-sp-orders
..\.venv\Scripts\python.exe app.py
```

Terminal 3, Gateway:

```powershell
cd .\api-gateway
..\.venv\Scripts\python.exe app.py
```

Se ejecuta **un proceso por aplicación**, con hilos, sin depurador ni recargador
automático. El gateway puede atender la llamada de Pedidos mientras espera su
respuesta original. Detén cada aplicación con `Ctrl+C`. El servidor de desarrollo
de Flask es únicamente para esta práctica local.

## Configuración y timeouts

| Aplicación | Variable | Valor predeterminado |
|---|---|---|
| Gateway | `ORDERS_SERVICE_URL` | `http://127.0.0.1:5001` |
| Gateway | `INVENTORIES_SERVICE_URL` | `http://127.0.0.1:5002` |
| Gateway | `CONNECT_TIMEOUT` | `1` |
| Gateway | `ORDERS_TIMEOUT` | `10` |
| Gateway | `INVENTORIES_TIMEOUT` | `2` |
| Pedidos | `API_GATEWAY_URL` | `http://127.0.0.1:5000` |
| Pedidos | `CONNECT_TIMEOUT` | `1` |
| Pedidos | `VALIDATION_TIMEOUT` | `5` |

Los tiempos están en segundos. `requests` recibe `(conexión, lectura)`; el segundo
limita la espera sin recibir datos, no constituye un plazo total para cuerpos que
se reciben lentamente. Inventario no conoce URLs de otros servicios.

Al personalizarlos conserva margen:

```text
VALIDATION_TIMEOUT de Pedidos > conexión del gateway + INVENTORIES_TIMEOUT
ORDERS_TIMEOUT del gateway > conexión de Pedidos + VALIDATION_TIMEOUT + margen
```

Los valores iniciales permiten que Pedidos registre y devuelva `ERROR_VALIDACION`
antes de expirar la llamada original. El gateway comprueba un mínimo de margen
entre sus propios timeouts al iniciar; debes mantener coherentes las configuraciones
de ambas aplicaciones. No hay reintentos automáticos ni redirecciones HTTP.

Los destinos son orígenes HTTP sin rutas, consultas ni credenciales. El gateway
mantiene rutas explícitas, no acepta URLs destino desde el cliente y bloquea
saltos repetidos con `X-Gateway-Route`. Los destinos de ambos servicios deben ser distintos.

## Contratos y documentación

| Aplicación | Swagger UI | Contrato | Salud local |
|---|---|---|---|
| Gateway | http://127.0.0.1:5000/docs | http://127.0.0.1:5000/openapi.yaml | http://127.0.0.1:5000/health |
| Pedidos | http://127.0.0.1:5001/docs | http://127.0.0.1:5001/openapi.yaml | http://127.0.0.1:5001/health |
| Inventario | http://127.0.0.1:5002/docs | http://127.0.0.1:5002/openapi.yaml | http://127.0.0.1:5002/health |

Swagger UI descarga sus recursos de un CDN con versión fijada; su interfaz requiere
Internet en el navegador. Los contratos y APIs funcionan sin esa descarga.
`/health` informa solo de la aplicación local, sin llamar a otros servicios.

Los contratos se escribieron y validaron **antes** de implementar las aplicaciones.
`openapi-core` los carga al iniciar. `ContractView` hereda de `MethodView`, valida la
solicitud antes de ejecutar la operación y valida su respuesta después. Marshmallow
transforma UUID y serializa modelos; no genera el contrato.

Los contratos incluyen objetos sin propiedades adicionales, enteros positivos,
UUID, nulos, estados y fechas UTC terminadas en `Z`. `/docs` y `/openapi.yaml` quedan
fuera de la validación de negocio. Las pruebas validan ejemplos, rutas/métodos y
compatibilidad de cuerpos y respuestas entre gateway y servicios.

## Probar desde una cuarta terminal

Todas las solicitudes de negocio de estos ejemplos apuntan al gateway:

```powershell
$baseUrl = "http://127.0.0.1:5000"
Invoke-RestMethod "$baseUrl/health"
Invoke-RestMethod "$baseUrl/api/v1/inventories"

# Confirmado: descuenta dos cafés de los diez iniciales.
$order = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -ContentType "application/json" -Body '{"product_id":1,"quantity":2}'
$order
Invoke-RestMethod "$baseUrl/api/v1/orders/$($order.id)"
Invoke-RestMethod "$baseUrl/api/v1/orders"
Invoke-RestMethod "$baseUrl/api/v1/inventories/1"

# Rechazado por stock insuficiente, sin modificar existencias.
Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -ContentType "application/json" -Body '{"product_id":1,"quantity":100}'

# Rechazado por producto inexistente.
Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -ContentType "application/json" -Body '{"product_id":999,"quantity":1}'

# HTTP 400: no crea un pedido. Invoke-RestMethod mostrará el error HTTP.
Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -ContentType "application/json" -Body '{"product_id":1,"quantity":0}'
```

Para un fallo técnico, detén solamente Inventario y crea un pedido válido.
Recibirás **201** con `ERROR_VALIDACION` y `No se pudo completar la validación`.
Un GET de inventario mediante el gateway devolverá 502 por conexión fallida o 504
si la conexión agota su timeout. Reiniciar Inventario restablece sus existencias.

| Ruta | Métodos | Respuestas principales |
|---|---|---|
| `/api/v1/orders` | POST, GET | Crear (201), listar (200) |
| `/api/v1/orders/{order_id}` | GET | Consultar UUID (200/404) |
| `/api/v1/inventories` | GET | Listar productos (200) |
| `/api/v1/inventories/{product_id}` | GET | Consultar producto (200/404) |
| `/api/v1/inventories/deductions` | POST | Descontar (200), inexistente (404), conflicto (409) |

El gateway publica las mismas operaciones y conserva método, ruta, consultas
repetidas, cuerpo y respuestas válidas. Elimina encabezados de conexión, `Host` y
`Content-Length`. Una respuesta fuera de contrato se registra y se convierte en
500 en un servicio o 502 (`INVALID_RESPONSE`) en el gateway, sin exponer trazas.

### Estados del pedido

| Estado | Significado |
|---|---|
| `CREADO` | Guardado y pendiente de validar; transitorio |
| `CONFIRMADO` | Inventario confirmó el descuento |
| `RECHAZADO` | Producto inexistente o stock insuficiente |
| `ERROR_VALIDACION` | Fallo técnico: no se conoce un resultado válido |

El flujo es **síncrono**: la creación espera el resultado HTTP antes de responder.
Normalmente el cliente no observa `CREADO`. Un pedido guardado devuelve 201 incluso
si queda rechazado o con error técnico. Una solicitud inválida devuelve 400 sin
crear pedido; los booleanos no se aceptan como enteros.

### Idempotencia del descuento

```powershell
$deduction = @{ order_id = $order.id; product_id = 1; quantity = 2 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/inventories/deductions" -ContentType "application/json" -Body $deduction
```

Si el pedido ya fue confirmado, devuelve su resultado anterior sin descontar otra
vez. El stock de esa respuesta corresponde al momento del descuento original.
Reutilizar el UUID con otro producto o cantidad devuelve 409 y `IDEMPOTENCY_CONFLICT`.
Solo se registran descuentos exitosos.

Inventario comienza con **Café: 10, Té: 5 y Chocolate: 0**. Un solo lock protege la
comprobación de duplicados, stock, descuento y registro del resultado. Las consultas
también usan el lock. Los rechazos no modifican existencias.

### Formato de errores

```json
{
  "code": "INSUFFICIENT_STOCK",
  "message": "Stock insuficiente",
  "details": {"product_id": 1}
}
```

| Situación | HTTP | Código |
|---|---|---|
| Entrada inválida o JSON malformado | 400 | `INVALID_INPUT` |
| POST con contenido distinto de JSON | 415 | `UNSUPPORTED_MEDIA_TYPE` |
| Producto inexistente | 404 | `PRODUCT_NOT_FOUND` |
| Pedido inexistente | 404 | `ORDER_NOT_FOUND` |
| Stock insuficiente | 409 | `INSUFFICIENT_STOCK` |
| UUID de descuento reutilizado con otros datos | 409 | `IDEMPOTENCY_CONFLICT` |
| Conexión fallida en gateway | 502 | `SERVICE_UNAVAILABLE` |
| Respuesta inválida en gateway | 502 | `INVALID_RESPONSE` |
| Timeout en gateway | 504 | `UPSTREAM_TIMEOUT` |
| Error interno | 500 | `INTERNAL_ERROR` |

Las rutas desconocidas y métodos no permitidos devuelven 404/405 con el mismo
formato. Un fallo de comunicación nunca se interpreta como stock insuficiente.

## Ejecutar las pruebas

Desde la raíz, **con los puertos 5000, 5001 y 5002 libres**:

```powershell
.\.venv\Scripts\python.exe scripts\verify.py
```

El comando ejecuta cuatro suites en procesos separados para evitar mezclar los
paquetes `api`. La última levanta las tres aplicaciones y comprueba HTTP real,
concurrencia, caída de Inventario y timeout con un sustituto HTTP lento usado solo
en la prueba. Cierra únicamente los procesos que ella misma inició.

Un `python -m pytest` desde la raíz ejecuta solo la suite global, según `pytest.ini`.
Usa `scripts/verify.py` para comprobar también las tres suites individuales.

Para una suite individual desde la raíz:

```powershell
Push-Location .\onb-msa-sp-orders
..\.venv\Scripts\python.exe -m pytest test -v
Pop-Location
```

Sustituye la carpeta por `api-gateway` o `onb-msa-sp-inventories` para sus pruebas.
Solo contratos y ejemplos, sin servidores:

```powershell
.\.venv\Scripts\python.exe -m pytest test\test_contracts.py -v
```

Las pruebas cubren estados, entradas sin efectos, errores de transporte, destino
HTTP de Pedidos, idempotencia y stock bajo concurrencia, instancias independientes,
respuestas inválidas, encabezados, consultas, rutas y compatibilidad de contratos.

## Limitaciones

- Al reiniciar se pierden todos los pedidos, descuentos registrados y cambios de
  stock. Cada aplicación crea sus repositorios una vez por instancia, no por solicitud.
- Varias instancias o procesos tendrían memorias y locks diferentes; el stock y
  la idempotencia no estarían coordinados. Esta práctica requiere un proceso por app.
- Una respuesta perdida deja un resultado incierto: Inventario podría haber
  descontado antes de perderse la respuesta. `ERROR_VALIDACION` no revierte el
  descuento. No hay recuperación, compensación ni conciliación automática.
- Repetir el POST de creación genera un nuevo UUID y puede descontar otra vez.
  La idempotencia cubre el descuento por `order_id`, no la creación de pedidos.
- No se usa base de datos, ORM, Redis, archivos de persistencia, Docker, Kafka,
  autenticación ni frontend. Los contratos y logs no son almacenamiento de negocio.

## Otro material del repositorio

Los fundamentos se conservan en la rama
[`programming_fundamentals`](https://github.com/keax-dev/coe-ing/tree/programming_fundamentals).

Referencias: [integración Flask de openapi-core](https://python-openapi.org/openapi-core/docs/latest/integrations/flask/)
y [vistas de clase de Flask](https://flask.palletsprojects.com/en/stable/views/).
