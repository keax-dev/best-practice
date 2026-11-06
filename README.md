# Microservicios Flask: Autenticación, Pedidos, Inventario y API Gateway

Práctica de componentes backend con **Python 3.14.7**, Flask, Marshmallow y
contratos **OpenAPI 3.0.3 definidos antes del código (contract-first)**.
Rama: `types_backend_components`.

## Cómo usar esta guía

Si es la primera vez, sigue los pasos 1 a 8 en orden. Si ya instalaste todo,
puedes ir directamente al [arranque de las cuatro aplicaciones](#paso-6-levantar-las-cuatro-aplicaciones)
y después al [login](#paso-7-comprobar-salud-e-iniciar-sesión).
Para verificar el proyecto usa la sección de [pruebas](#paso-5-ejecutar-las-pruebas).

El orden completo es: **requisitos → entorno y dependencias → comprobación de
generación → claves → configuración opcional → pruebas → cuatro servidores →
login y solicitudes**. Usa una quinta terminal para probar las APIs; las otras
cuatro permanecen ocupadas por los servidores.

| Necesitas… | Consulta |
|---|---|
| Entender el recorrido y los roles | [Arquitectura](#objetivo-y-recorrido) e [identidad](#identidad-roles-y-confianza-entre-aplicaciones) |
| Preparar una máquina nueva | [Requisitos](#paso-1-comprobar-requisitos-y-obtener-el-código), [dependencias](#paso-2-crear-el-entorno-e-instalar-las-cuatro-aplicaciones) y [claves](#paso-3-generar-las-claves-locales) |
| Cambiar URLs, claves o timeouts | [Configuración](#paso-4-configuración-opcional-con-env) |
| Probar permisos con admin y cliente | [Ejemplos de pedidos](#paso-8-crear-y-consultar-pedidos-con-ambos-roles) |
| Abrir Swagger y los contratos | [Documentación de las APIs](#contratos-y-swagger-ui) |
| Resolver un fallo de arranque o autenticación | [Solución de problemas](#solución-de-problemas) |

La API que consume el usuario es el **gateway en el puerto 5000**. No necesitas
enviar `X-User-Id`, `X-User-Role` ni claves internas desde PowerShell o Swagger:
el gateway establece esos encabezados después de autenticarte.

## Objetivo y recorrido

Iniciar sesión, crear pedidos en memoria y descontar existencias. El gateway
centraliza la validación JWT y los permisos de rutas; cada servicio conserva
su responsabilidad de negocio y su propia memoria.

```text
LOGIN
Usuario → Gateway :5000 → Autenticación :5003 → JWT firmado con RS256

CREACIÓN DE PEDIDO
Usuario con JWT → Gateway → Pedidos :5001
Usuario         ← Gateway ← HTTP 201 con user_id y estado CREADO

VALIDACIÓN EN SEGUNDO PLANO
Trabajador de Pedidos → Gateway → Inventario :5002
                                 descuento atómico e idempotente
Trabajador de Pedidos ← Gateway ← resultado del descuento
       │ actualiza el pedido en memoria
       ▼
CONFIRMADO / CANCELADO / ERROR_VALIDACION

CONSULTA POSTERIOR
Usuario con JWT → Gateway → GET de Pedidos → estado actualizado
```

El recorrido de negocio sigue siendo **Cliente → Gateway → Pedidos → Gateway →
Inventario**. El cliente puede crear pedidos sin tener permiso para consumir
Inventario directamente.

| Aplicación | Puerto | Responsabilidad |
|---|---|---|
| `api-gateway` | 5000 | Validar JWT, autorizar rutas y reenviar HTTP |
| `onb-msa-sp-orders` | 5001 | Guardar pedidos, controlar propiedad y coordinar descuentos en segundo plano |
| `onb-msa-sp-inventories` | 5002 | Consultar productos y descontar stock con un lock |
| `onb-msa-sp-auth` | 5003 | Validar contraseñas de dos usuarios y emitir JWT |

## Identidad, roles y confianza entre aplicaciones

Los únicos usuarios están definidos en `onb-msa-sp-auth/api/seed.py`. Sus
contraseñas se almacenan en código como hashes de Werkzeug.

| Usuario | Contraseña de demostración | `sub` / `user_id` | Rol |
|---|---|---|---|
| `admin` | `Admin123!` | `user-admin` | `ADMIN` |
| `client` | `Client123!` | `user-client` | `CLIENT` |

Estas cuentas son exclusivamente para el ejercicio local.

| Operación | ADMIN | CLIENT |
|---|---|---|
| Crear un pedido | Sí, con su propio `user_id` | Sí, con su propio `user_id` |
| Listar pedidos | Todos | Solo los propios |
| Consultar un pedido | Cualquiera | Solo si es suyo; otro devuelve 404 |
| Consultar Inventario | Sí | No, devuelve 403 |
| Solicitar descuentos directamente | Sí | No, devuelve 403 |

El cuerpo de creación solo acepta `product_id` y `quantity`. **No acepta
`user_id`, `client_id` ni `customer_id`**: el propietario sale del `sub` del JWT
validado y no se puede elegir desde el cuerpo ni mediante parámetros de consulta.

La autenticación se distribuye así:

1. Autenticación firma JWT con su clave privada RSA. El token incluye `sub`,
   `role`, `iat`, `exp`, `iss` y `aud`; no incluye la contraseña.
2. El gateway verifica localmente firma RS256, claims obligatorios, vencimiento,
   emisor, audiencia y formato de identidad. No consulta el login en cada solicitud.
3. El gateway elimina `Authorization` y los encabezados internos recibidos del
   usuario; establece `X-User-Id` y `X-User-Role` a partir de la identidad verificada,
   y añade `X-Internal-Key` al reenviar a Pedidos o Inventario.
4. Los servicios **no validan JWT**. Comprueban la clave interna del gateway y la
   identidad recibida. Pedidos además comprueba la propiedad del pedido. Entrar
   directamente en los puertos 5001/5002 con un JWT o una identidad inventada no basta.
5. Para descontar, Pedidos llama al gateway con `X-Orders-Service-Key`, una
   credencial diferente de la clave anterior. Solo permite
   `POST /api/v1/inventories/deductions`. El gateway reenvía esa operación con
   identidad `orders-service` y rol `SERVICE`. Ese rol no puede listar inventario
   ni operar con pedidos. No se usa el JWT del cliente para esta llamada interna.

La clave pública verifica firmas pero no permite emitir JWT. La clave privada
solo la carga Autenticación; Pedidos e Inventario no necesitan claves JWT.
Los encabezados internos solo son confiables acompañados de la clave interna.
Si alguien obtiene esa clave podría suplantar identidad interna: no debe publicarse.

## Paso 1. Comprobar requisitos y obtener el código

Necesitas Windows con PowerShell, Git y Python 3.14.7. Para instalar dependencias
necesitas Internet. No se necesita base de datos, Docker, Redis ni migraciones.
La generación de las cuatro APIs y sus pruebas de regeneración utilizan **Java 21** y
OpenAPI Generator. Para ejecutar las APIs con los archivos ya generados basta Python.

```powershell
git --version
py -3.14 --version
java -version
```

El segundo comando debe mostrar `Python 3.14.7` para reproducir el entorno
verificado. Si `py` no se reconoce, instala Python con su lanzador para Windows
y abre otra terminal. No copies `.venv` de otra computadora: créala en la nueva.
`java -version` debe mostrar Java 21. Si no se reconoce, instala un JDK 21,
añade su carpeta `bin` al `PATH` y abre PowerShell de nuevo antes de continuar.

Si todavía no tienes el repositorio:

```powershell
cd "$env:USERPROFILE\Documents"
git clone --branch types_backend_components https://github.com/keax-dev/coe-ing.git
cd .\coe-ing
```

Si ya lo tienes, comprueba tus cambios antes de actualizar:

```powershell
cd C:\Users\jimen\Documents\coe-ing
git status
git switch types_backend_components
git pull --ff-only origin types_backend_components
```

Si Git indica que tus cambios impiden continuar, consérvalos y resuelve el problema
sin descartarlos. En otra computadora cambia la ruta por la de tu repositorio.
Los siguientes pasos parten de la raíz `coe-ing`.

## Paso 2. Crear el entorno e instalar las cuatro aplicaciones

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r .\requirements-codegen.txt
.\.venv\Scripts\python.exe -m pip check
```

Si `.venv` ya usa Python 3.14.7, omite su creación. `pip check` debe mostrar
`No broken requirements found.`. No hace falta activar el entorno ni cambiar la
política de ejecución de PowerShell. Las dependencias directas tienen versiones
fijadas; `pytest` se instala con esos archivos. Repite la instalación cuando cambien.

Compartir el entorno virtual facilita la práctica; las aplicaciones siguen siendo
procesos independientes. También pueden usar entornos separados instalando el
`requirements.txt` correspondiente en cada uno. El script de preparación de claves
requiere `cryptography`, incluido en las dependencias de Autenticación y Gateway.

El `requirements-codegen.txt` de la raíz incluye las dependencias de ejecución de
las cuatro aplicaciones y fija OpenAPI Generator 7.27.0 y Ruff 0.17.3. Cada app
también tiene su propio `requirements-codegen.txt` para desarrollarla por separado.
Para ejecutar una app con los archivos ya generados basta su `requirements.txt`;
para ejecutar todas las pruebas necesitas las herramientas de generación y Java en `PATH`.

Antes de continuar, comprueba que los archivos generados coincidan con los contratos:

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_apis.py --check
```

Debe aparecer `generated files match the contract and templates` para las cuatro
aplicaciones. Si faltan archivos o están desactualizados, regenera y comprueba otra vez:

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_apis.py
.\.venv\Scripts\python.exe .\scripts\generate_apis.py --check
```

No necesitas regenerar en cada arranque: hazlo cuando cambien contratos,
configuración o plantillas de generación. Si cambiaron las firmas, adapta también
las implementaciones; el generador no escribe la lógica de negocio.

## Paso 3. Generar las claves locales

```powershell
.\.venv\Scripts\python.exe scripts\setup_local.py
```

Crea esta configuración, excluida de Git:

```text
.secrets/
  jwt-private.pem       # firma: Autenticación
  jwt-public.pem        # verificación: Gateway
  internal-api.key      # Gateway → Pedidos/Inventario
  orders-service.key    # Pedidos → Gateway, solo para descuentos
```

Puedes repetir el comando: conserva los secretos existentes y comprueba que las
claves pública y privada coincidan. No subas ni compartas `.secrets`. En otra máquina
ejecuta de nuevo el script para generar sus propias claves. Si faltan, las aplicaciones
protegidas no arrancarán; no existe una clave insegura predeterminada.

Las claves son configuración, no persistencia de pedidos o stock. Si necesitas
rotarlas, detén las cuatro aplicaciones y conserva o mueve de forma controlada la
configuración anterior antes de generar otra. Reinicia después todas las apps;
los JWT firmados con la clave anterior dejarán de ser válidos.

## Paso 4. Configuración opcional con `.env`

Los valores predeterminados ya funcionan. Para crear archivos editables sin
sobrescribir los existentes:

```powershell
foreach ($application in @('api-gateway', 'onb-msa-sp-orders', 'onb-msa-sp-inventories', 'onb-msa-sp-auth')) {
    $localConfig = Join-Path $application '.env'
    if (-not (Test-Path $localConfig)) {
        Copy-Item (Join-Path $application '.env.example') $localConfig
    }
}
```

Cada aplicación carga su propio `.env`. Las variables del entorno tienen prioridad.
Los `.env` no se suben a Git.

| Aplicación | Variable | Valor predeterminado |
|---|---|---|
| Gateway | `ORDERS_SERVICE_URL` | `http://127.0.0.1:5001` |
| Gateway | `INVENTORIES_SERVICE_URL` | `http://127.0.0.1:5002` |
| Gateway | `AUTH_SERVICE_URL` | `http://127.0.0.1:5003` |
| Gateway | `CONNECT_TIMEOUT` | `1` segundo |
| Gateway | `ORDERS_TIMEOUT` | `10` segundos |
| Gateway | `INVENTORIES_TIMEOUT` | `2` segundos |
| Gateway | `AUTH_TIMEOUT` | `3` segundos |
| Pedidos | `API_GATEWAY_URL` | `http://127.0.0.1:5000` |
| Pedidos | `CONNECT_TIMEOUT` | `1` segundo |
| Pedidos | `VALIDATION_TIMEOUT` | `5` segundos |
| Pedidos | `VALIDATION_WORKERS` | `4` trabajadores simultáneos; entero positivo |
| Auth y Gateway | `JWT_ISSUER` | `coe-auth` |
| Auth y Gateway | `JWT_AUDIENCE` | `coe-backend` |
| Auth | `JWT_ACCESS_TTL` | `900` segundos (15 minutos) |

Para cambiar rutas de secretos usa rutas absolutas:

| Variable opcional | Aplicaciones que la utilizan |
|---|---|
| `JWT_PRIVATE_KEY_FILE` | Auth |
| `JWT_PUBLIC_KEY_FILE` | Gateway |
| `INTERNAL_API_KEY_FILE` | Gateway, Pedidos, Inventario |
| `ORDERS_SERVICE_KEY_FILE` | Gateway, Pedidos |

Las rutas predeterminadas apuntan a `.secrets` en la raíz del repositorio,
independientemente de la terminal desde la que ejecutes `app.py`.
También se pueden proporcionar `INTERNAL_API_KEY` y `ORDERS_SERVICE_KEY` mediante
el entorno en lugar de archivos. Deben tener al menos 32 caracteres y coincidir
entre sus consumidores. El generador crea valores aleatorios más largos.

Los destinos HTTP no admiten rutas, consultas ni credenciales y deben ser distintos.
Inventario no conoce las URLs de los demás servicios.
Los puertos de escucha están definidos en cada `app.py`: 5000, 5001, 5002 y 5003.
Modificar una URL en `.env` solo cambia el destino de las llamadas HTTP; no cambia
el puerto en el que arranca el servidor. Para seguir esta guía conserva esos puertos.

`requests` utiliza `(timeout de conexión, timeout de lectura)`; el segundo limita
la espera sin datos, no el tiempo total de una respuesta que envía datos lentamente.
Para dar tiempo al gateway a responder antes de que el trabajador abandone la llamada,
conserva este margen:

```text
VALIDATION_TIMEOUT de Pedidos > conexión del gateway + INVENTORIES_TIMEOUT
```

`ORDERS_TIMEOUT` limita las solicitudes HTTP del gateway a Pedidos, que ahora
responde sin esperar a Inventario. Ya no necesita cubrir el recorrido interno
completo. Un fallo posterior del descuento se registra en el pedido y se conoce
mediante GET. No hay reintentos automáticos ni redirecciones HTTP.

## Paso 5. Ejecutar las pruebas

Si levantaste las aplicaciones manualmente, detén las cuatro con `Ctrl+C` en sus
terminales. Los puertos **5000, 5001, 5002 y 5003 deben estar libres**.
Desde la raíz ejecuta:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\scripts\verify.py
```

Ejecuta cinco suites en procesos separados: Auth, Gateway, Pedidos, Inventario y
pruebas globales. Esto evita mezclar los paquetes `api` de aplicaciones diferentes.
Las pruebas usan repositorios y credenciales aislados; la prueba global genera
claves temporales, inicia cuatro procesos reales y los cierra al terminar.

La suite actual contiene **134 pruebas**:

| Suite | Pruebas |
|---|---:|
| Autenticación, incluida generación | 21 |
| API Gateway | 32 |
| Pedidos | 46 |
| Inventario | 26 |
| Contratos, preparación de claves y recorrido HTTP completo | 9 |
| **Total** | **134** |

Verás una sección `Checking ...` por suite y su resumen `passed`. Si una falla,
el script se detiene y muestra el error; no debes interpretar los resúmenes de las
suites anteriores como una verificación completa. Las pruebas no modifican tus
claves de `.secrets`. Al terminar tampoco dejan las aplicaciones disponibles:
para usarlas manualmente debes arrancarlas con el paso 6.

Si quieres conservar tus servidores abiertos, puedes ejecutar la verificación
en cuatro puertos alternativos libres (5100–5103). Solo cambia los servidores de
la prueba; tus aplicaciones locales conservan sus puertos:

```powershell
$env:TEST_BASE_PORT = '5100'
try {
    .\.venv\Scripts\python.exe .\scripts\verify.py
} finally {
    Remove-Item Env:TEST_BASE_PORT
}
```

Para ejecutar una suite individual desde la raíz:

```powershell
Push-Location .\onb-msa-sp-auth
..\.venv\Scripts\python.exe -m pytest test -v
Pop-Location
```

Cambia la carpeta por `api-gateway`, `onb-msa-sp-orders` o
`onb-msa-sp-inventories` para probar otra aplicación. Ejecuta cada suite desde su
carpeta: todas usan un paquete llamado `api` y no se deben mezclar en un único
proceso de pytest.

Desde la raíz, este comando ejecuta **solo las 9 pruebas globales**, según `pytest.ini`:

```powershell
.\.venv\Scripts\python.exe -m pytest test -v
```

También necesita los cuatro puertos libres porque incluye el recorrido real.
Para revisar **solo los contratos**, sin levantar servidores:

```powershell
.\.venv\Scripts\python.exe -m pytest test\test_contracts.py -v
```

Las pruebas cubren login y hashes, firma y claims JWT, tokens vencidos/alterados,
roles, suplantación por encabezados, acceso directo a servicios, propiedad de pedidos,
credencial de servicio limitada, entradas sin efectos, errores HTTP, respuestas
fuera de contrato, idempotencia, concurrencia, stock no negativo, caída de Inventario
y timeout real. Comprueban que POST devuelve `CREADO` incluso con Inventario
bloqueado, la posterior transición de estado y el límite de trabajadores.
También verifican rutas y compatibilidad de los cuatro contratos.

## Paso 6. Levantar las cuatro aplicaciones

Abre **cuatro terminales distintas**. Estos comandos parten de la raíz; ajusta la
ruta si clonaste el repositorio en otro lugar.

Terminal 1, Autenticación:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\onb-msa-sp-auth\app.py
```

Terminal 2, Inventario:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\onb-msa-sp-inventories\app.py
```

Terminal 3, Pedidos:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\onb-msa-sp-orders\app.py
```

Terminal 4, Gateway:

```powershell
cd C:\Users\jimen\Documents\coe-ing
.\.venv\Scripts\python.exe .\api-gateway\app.py
```

Mantén las terminales abiertas. Cada comando ocupa su terminal hasta pulsar `Ctrl+C`.
Debes ver `Running on http://127.0.0.1:` con su puerto correspondiente.
El aviso de Flask sobre el servidor de desarrollo es normal: se usa solo para la
práctica local. Cada app ejecuta **un proceso con hilos, sin debug ni recargador**.
El gateway puede atender una llamada interna mientras espera la respuesta de Pedidos.
Espera a que las cuatro terminales indiquen que sus servidores están escuchando
antes de hacer login. Un `/health` correcto del gateway no comprueba si los otros
tres servidores están disponibles.

## Paso 7. Comprobar salud e iniciar sesión

Abre una **quinta terminal**:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
Invoke-RestMethod http://127.0.0.1:5001/health
Invoke-RestMethod http://127.0.0.1:5002/health
Invoke-RestMethod http://127.0.0.1:5003/health

$baseUrl = 'http://127.0.0.1:5000'
$clientLogin = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/auth/login" -ContentType 'application/json' -Body '{"username":"client","password":"Client123!"}'
$clientHeaders = @{ Authorization = "Bearer $($clientLogin.access_token)" }

$adminLogin = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/auth/login" -ContentType 'application/json' -Body '{"username":"admin","password":"Admin123!"}'
$adminHeaders = @{ Authorization = "Bearer $($adminLogin.access_token)" }
```

Cada health devuelve `status: ok` y solo comprueba su aplicación local. El login,
health, `/docs` y `/openapi.yaml` son públicos. Todas las demás operaciones
requieren autenticación. Cuando expire un JWT repite su login y reconstruye sus
encabezados. No se realizan peticiones al login automáticamente.

La respuesta de login tiene esta forma; `access_token` contendrá el JWT real:

```json
{
  "access_token": "<JWT firmado por Autenticación>",
  "token_type": "Bearer",
  "expires_in": 900
}
```

En las operaciones protegidas, el encabezado que envías es:

```http
Authorization: Bearer <access_token>
```

`$clientHeaders` y `$adminHeaders` ya construyen ese encabezado. Mantén sus valores
separados para probar los permisos de cada usuario. Si abres otra terminal, vuelve
a ejecutar el bloque de login para crear esas variables en la nueva sesión.

## Paso 8. Crear y consultar pedidos con ambos roles

```powershell
# El cliente crea un pedido propio; el user_id no se envía.
$clientOrder = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -Headers $clientHeaders -ContentType 'application/json' -Body '{"product_id":1,"quantity":2}'
$clientOrder | Format-List

# El cliente solo ve sus pedidos.
Invoke-RestMethod "$baseUrl/api/v1/orders" -Headers $clientHeaders
Invoke-RestMethod "$baseUrl/api/v1/orders/$($clientOrder.id)" -Headers $clientHeaders

# El administrador crea su propio pedido y puede consultar todos.
$adminOrder = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -Headers $adminHeaders -ContentType 'application/json' -Body '{"product_id":2,"quantity":1}'
Invoke-RestMethod "$baseUrl/api/v1/orders" -Headers $adminHeaders
Invoke-RestMethod "$baseUrl/api/v1/orders/$($clientOrder.id)" -Headers $adminHeaders
Invoke-RestMethod "$baseUrl/api/v1/inventories" -Headers $adminHeaders
```

El primer POST devuelve HTTP 201 con `CREADO`, `user_id: user-client` y `reason`
nulo. Con Inventario disponible, después pasa a `CONFIRMADO` y deja café con stock 8.
Un GET inmediato puede devolver todavía `CREADO` o encontrar la validación ya terminada.
Repetir la creación genera un UUID nuevo y vuelve a consumir existencias.

La respuesta del primer pedido será similar a esta; el UUID y la fecha se generan
en cada solicitud:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-client",
  "product_id": 1,
  "quantity": 2,
  "status": "CREADO",
  "reason": null,
  "created_at": "2026-11-05T12:00:00.000000Z"
}
```

Para esperar el resultado, define esta función en la quinta terminal y consulta
el UUID recibido. El límite es de 30 segundos; la espera del cliente no cancela
el pedido ni su validación:

```powershell
function Wait-Order {
    param([string]$OrderId, [hashtable]$Headers)
    $deadline = (Get-Date).AddSeconds(30)
    do {
        $order = Invoke-RestMethod "$baseUrl/api/v1/orders/$OrderId" -Headers $Headers -TimeoutSec 5
        if ($order.status -ne 'CREADO') { return $order }
        Start-Sleep -Milliseconds 250
    } while ((Get-Date) -lt $deadline)
    throw "El pedido $OrderId sigue pendiente; puedes volver a consultarlo."
}

$clientOrder = Wait-Order -OrderId $clientOrder.id -Headers $clientHeaders
$clientOrder | Format-List
Invoke-RestMethod "$baseUrl/api/v1/inventories/1" -Headers $adminHeaders
```

En Swagger, el procedimiento equivalente es copiar el `id` del POST y ejecutar
`GET /api/v1/orders/{order_id}` hasta que deje de mostrar `CREADO`. No hay notificación
push ni actualización automática de la pantalla.

El `user_id` de esa respuesta identifica al propietario. Un JWT del administrador
produce `user-admin`; uno del cliente produce `user-client`. El rol no cambia el
propietario al crear: el administrador puede consultar pedidos ajenos, pero este
ejercicio no ofrece creación de pedidos en nombre de otro usuario.

Los siguientes ejemplos devuelven errores intencionales. PowerShell mostrará un
error HTTP, ya que `Invoke-RestMethod` no devuelve normalmente los cuerpos de error:

```powershell
# 403: el cliente no puede consumir Inventario.
Invoke-RestMethod "$baseUrl/api/v1/inventories" -Headers $clientHeaders

# 404: el cliente no puede consultar un pedido del administrador.
Invoke-RestMethod "$baseUrl/api/v1/orders/$($adminOrder.id)" -Headers $clientHeaders

# 400: no se puede elegir propietario en el cuerpo ni enviar cantidades inválidas.
Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -Headers $clientHeaders -ContentType 'application/json' -Body '{"product_id":1,"quantity":1,"user_id":"user-admin"}'
Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -Headers $clientHeaders -ContentType 'application/json' -Body '{"product_id":1,"quantity":0}'

# 401: falta el JWT.
Invoke-RestMethod "$baseUrl/api/v1/orders"
```

Casos de negocio que también responden HTTP 201 con `CREADO` y luego se cancelan:

```powershell
# CANCELADO al consultar: stock insuficiente, sin modificar existencias.
$cancelledOrder = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -Headers $clientHeaders -ContentType 'application/json' -Body '{"product_id":1,"quantity":100}'
Wait-Order -OrderId $cancelledOrder.id -Headers $clientHeaders

# CANCELADO al consultar: producto inexistente.
$missingProductOrder = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -Headers $clientHeaders -ContentType 'application/json' -Body '{"product_id":999,"quantity":1}'
Wait-Order -OrderId $missingProductOrder.id -Headers $clientHeaders
```

Para un fallo técnico, detén solamente Inventario y crea un pedido válido: recibirás
201 con `CREADO`. Al consultar después, verás `ERROR_VALIDACION` y
`No se pudo completar la validación`. Un GET autorizado
de inventario devolverá 502 por conexión fallida o 504 si la conexión agota el timeout.
Reiniciar Inventario restablece sus existencias y olvida sus descuentos anteriores.

Pasos exactos, después de ejecutar el login del paso 7:

1. En la terminal 2 (Inventario), pulsa `Ctrl+C`. Deja las otras tres aplicaciones ejecutándose.
2. En la quinta terminal, ejecuta:

```powershell
$failedOrder = Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/orders" -Headers $clientHeaders -ContentType 'application/json' -Body '{"product_id":1,"quantity":1}'
$failedOrder = Wait-Order -OrderId $failedOrder.id -Headers $clientHeaders
$failedOrder | Format-List
```

3. Comprueba `status: ERROR_VALIDACION`; ese pedido permanece guardado.
4. En la terminal 2 vuelve a ejecutar el comando de Inventario del paso 6.
   El pedido anterior conserva su estado: no hay revalidación automática.

Para inspeccionar el cuerpo de un error HTTP en Windows PowerShell, puedes usar:

```powershell
try {
    Invoke-RestMethod "$baseUrl/api/v1/inventories" -Headers $clientHeaders -ErrorAction Stop
} catch {
    # En este ejemplo se espera HTTP 403 y code FORBIDDEN.
    [int]$_.Exception.Response.StatusCode
    $_.ErrorDetails.Message
}
```

## Contratos y Swagger UI

| Aplicación | Swagger UI | Contrato | Salud local |
|---|---|---|---|
| Gateway | http://127.0.0.1:5000/docs | http://127.0.0.1:5000/openapi.yaml | http://127.0.0.1:5000/health |
| Pedidos | http://127.0.0.1:5001/docs | http://127.0.0.1:5001/openapi.yaml | http://127.0.0.1:5001/health |
| Inventario | http://127.0.0.1:5002/docs | http://127.0.0.1:5002/openapi.yaml | http://127.0.0.1:5002/health |
| Auth | http://127.0.0.1:5003/docs | http://127.0.0.1:5003/openapi.yaml | http://127.0.0.1:5003/health |

Para practicar desde Swagger UI:

1. Abre http://127.0.0.1:5000/docs.
2. En `POST /api/v1/auth/login`, pulsa **Try it out**, introduce las credenciales
   de `admin` o `client` y ejecuta la operación.
3. Copia únicamente el valor de `access_token` de la respuesta.
4. Pulsa **Authorize**, pega el JWT en **BearerAuth** y confirma. Introduce solo
   el token: Swagger UI añade el prefijo `Bearer`.
5. Ejecuta las operaciones protegidas y comprueba los permisos del rol elegido.
6. Para cambiar de usuario, quita la autorización anterior, realiza el otro login
   y reemplaza el token en **Authorize**. Al vencer, repite el login.

No necesitas rellenar `OrdersServiceKey`: es una credencial exclusiva de Pedidos.
Las interfaces de los servicios documentan encabezados internos para inspeccionar
el contrato; el cliente utiliza siempre el gateway y no necesita conocer esas claves.

Swagger UI descarga recursos de un CDN con versión fijada; su interfaz requiere
Internet. Los contratos y las APIs funcionan sin esa descarga.

`openapi-core` carga los contratos al construir cada aplicación. `ContractView`
hereda de `MethodView`, aplica la autorización y valida solicitudes antes de
ejecutar efectos de negocio, y valida después las respuestas, incluidos los errores.
Las vistas se registran con `Blueprint`, `as_view()` y `add_url_rule()`.
Marshmallow transforma UUID y serializa modelos; no genera los contratos.

Los contratos incluyen ejemplos, referencias reutilizables, UUID, fechas UTC,
nulos, estados, cuerpos cerrados y esquemas de seguridad. Las diferencias entre
autenticación externa e interna se documentan en sus respectivos contratos; los
cuerpos y respuestas de negocio deben coincidir. Las pruebas detectan divergencias.
Los recursos de documentación quedan fuera de la validación de negocio.

## Generación desde OpenAPI: las cuatro aplicaciones

Cada aplicación genera DTO de request/response, esquemas Marshmallow, interfaz
abstracta y adaptadores `MethodView` desde su `contracts/openapi.yaml`. Health y
los errores también utilizan DTO generados. Los modelos de negocio, repositorios,
seguridad y lógica se implementan manualmente y consumen estas interfaces.

Desde la raíz, después de instalar `requirements-codegen.txt`:

```powershell
# Generar las cuatro aplicaciones.
.\.venv\Scripts\python.exe .\scripts\generate_apis.py

# Comprobar las cuatro sin modificar archivos.
.\.venv\Scripts\python.exe .\scripts\generate_apis.py --check

# Generar o comprobar solo Pedidos.
.\.venv\Scripts\python.exe .\scripts\generate_apis.py --app orders
.\.venv\Scripts\python.exe .\scripts\generate_apis.py --app orders --check
```

Los valores de `--app` son `auth`, `orders`, `inventories`, `gateway` y `all`.
`scripts/generate_auth.py` se conserva como acceso directo a `--app auth`.

El generador real es **OpenAPI Generator 7.27.0**, con plantillas compartidas en
`codegen/templates/`. Cada app tiene su configuración en `codegen/config.yaml`.
Se conservan Flask, `MethodView`, Marshmallow y `openapi-core`; no se añade Connexion.
Los artefactos se incluyen en Git y no se editan a mano. La generación se realiza
en un directorio temporal, comprueba sintaxis/formato y publica únicamente en
`api/generated/` de la aplicación seleccionada.

| Aplicación | Interfaz generada | Implementación manual |
|---|---|---|
| Auth | `AuthAPI` | `AuthAPIImpl` en `api/routes/auth.py` |
| Pedidos | `OrdersAPI` | `OrdersAPIImpl` en `api/routes/order.py` |
| Inventario | `InventoryAPI` | `InventoryAPIImpl` en `api/routes/inventory.py` |
| Gateway | `GatewayAPI` | `GatewayAPIImpl` en `api/routes/proxy.py` |

Las rutas generadas convierten UUID, enteros de URL, fechas y cuerpos en modelos
tipados. Los campos JSON enteros siguen siendo estrictos y no aceptan booleanos.
Las respuestas de lista y los campos nulos se serializan según el contrato.
El gateway consume la interfaz generada y conserva los códigos, cuerpos y
encabezados válidos de los servicios, con validación OpenAPI de la respuesta.

Pedidos también genera `api/generated/clients/inventory/` desde la operación de
descuento del **contrato del gateway**. Su cliente manual lo consume y decide el
estado del pedido. La URL HTTP de descuento y los DTO del cliente ya no se duplican
manualmente. Los secretos internos y timeouts se proporcionan al cliente al iniciarlo.

Al cambiar un contrato, regenera todo, adapta las implementaciones afectadas,
reinicia los procesos y ejecuta las pruebas. `--check` detecta artefactos modificados,
faltantes, sobrantes o desactualizados, incluido el cliente generado de Pedidos.
Las plantillas cubren las construcciones utilizadas en los contratos del ejercicio;
una construcción no soportada detiene la generación antes de publicar esa app.
Consulta la [guía de generación](codegen/README.md) y el [detalle de Auth](onb-msa-sp-auth/README.md).

## Operaciones, estados y errores

| Ruta | Métodos |
|---|---|
| `/api/v1/auth/login` | POST |
| `/api/v1/orders` | GET, POST |
| `/api/v1/orders/{order_id}` | GET |
| `/api/v1/inventories` | GET |
| `/api/v1/inventories/{product_id}` | GET |
| `/api/v1/inventories/deductions` | POST |

| Estado del pedido | Significado |
|---|---|
| `CREADO` | Guardado y pendiente de validar; estado de la respuesta de creación |
| `CONFIRMADO` | Inventario confirmó el descuento |
| `CANCELADO` | Producto inexistente o stock insuficiente |
| `ERROR_VALIDACION` | Fallo técnico; no se conoce un resultado válido |

El flujo es **asíncrono**: POST guarda el pedido, programa una tarea y devuelve
201 con una copia inmutable en estado `CREADO`. La tarea puede finalizar incluso
antes de que el cliente haga su primer GET; ese GET devuelve el estado actual.
El resultado final no modifica la respuesta del POST ya emitida. Entradas inválidas
no crean pedidos ni programan tareas; los booleanos no se aceptan como enteros.

Pedidos crea un `ThreadPoolExecutor` por instancia de aplicación, con cuatro
trabajadores por defecto. Los pedidos adicionales esperan en su cola en memoria.
Cada trabajador usa el cliente HTTP generado para llamar a Inventario mediante
el gateway, sin depender del contexto de la solicitud Flask ni del JWT del usuario.
El repositorio de pedidos ya protege lecturas y escrituras con un lock, y sus
modelos inmutables evitan modificar la respuesta inicial desde otro hilo.
No hay cancelación manual de pedidos ni recuperación automática de tareas fallidas.

Todos los errores siguen este formato, sin trazas internas:

```json
{"code": "INSUFFICIENT_STOCK", "message": "Stock insuficiente", "details": {"product_id": 1}}
```

| HTTP | Códigos principales |
|---|---|
| 400 | `INVALID_INPUT`: cuerpo inválido, JSON malformado o parámetros incorrectos |
| 401 | `AUTH_REQUIRED`, `INVALID_TOKEN`, `TOKEN_EXPIRED`, `INVALID_CREDENTIALS` |
| 403 | `FORBIDDEN`: autenticado sin permiso o identidad interna no admitida |
| 404 | `ORDER_NOT_FOUND`, `PRODUCT_NOT_FOUND`, `NOT_FOUND` |
| 405 | `METHOD_NOT_ALLOWED` |
| 409 | `INSUFFICIENT_STOCK`, `IDEMPOTENCY_CONFLICT` |
| 415 | `UNSUPPORTED_MEDIA_TYPE` |
| 500 | `INTERNAL_ERROR` |
| 502 | `SERVICE_UNAVAILABLE`, `INVALID_RESPONSE` en gateway |
| 504 | `UPSTREAM_TIMEOUT` en gateway |

Las respuestas fuera de contrato se registran en los logs y se convierten en 500
en un servicio o 502 en gateway. Un fallo de comunicación no significa falta de stock.
El gateway conserva método, ruta, consultas repetidas, cuerpo y respuestas válidas;
filtra encabezados de conexión, `Host`, `Content-Length` y credenciales internas.

## Memoria, concurrencia e idempotencia

Inventario comienza con **Café: 10, Té: 5 y Chocolate: 0**, definidos en `api/seed.py`.
Pedidos empieza vacío. Los repositorios se crean una vez por instancia de aplicación.

Un solo lock protege duplicados, comprobación de stock, descuento y registro del
éxito. No permite stock negativo y los rechazos no modifican existencias.
Los descuentos exitosos se registran por `order_id`: repetir el mismo UUID y datos
devuelve el resultado original sin descontar otra vez. Cambiar producto o cantidad
para ese UUID devuelve 409 `IDEMPOTENCY_CONFLICT`. Solo se guardan éxitos.

Para comprobarlo como administrador con el pedido del paso 8:

```powershell
$deduction = @{ order_id = $clientOrder.id; product_id = 1; quantity = 2 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$baseUrl/api/v1/inventories/deductions" -Headers $adminHeaders -ContentType 'application/json' -Body $deduction
```

El stock devuelto corresponde al descuento original, no a una consulta nueva.
La idempotencia protege descuentos identificados, no repeticiones del POST de creación.

## Estructura del código

```text
api-gateway/
  contracts/openapi.yaml
  codegen/config.yaml
  api/generated/{models, interfaces}/
  api/generated/{routes, runtime}.py
  api/{clients, routes}/
  api/{__init__, contract, errors, security}.py
  test/routes/
onb-msa-sp-auth/
  contracts/openapi.yaml
  codegen/config.yaml
  api/generated/{models, interfaces}/
  api/generated/{routes, runtime}.py
  api/generated/manifest.json
  api/{models, routes, services, repositories}/
  api/{__init__, contract, errors, security, seed}.py
  test/routes/
onb-msa-sp-orders/
  contracts/openapi.yaml
  codegen/config.yaml
  api/generated/{models, interfaces}/
  api/generated/clients/inventory/
  api/generated/{routes, runtime}.py
  api/{models, routes, services, repositories, clients}/
  api/{__init__, contract, errors, security}.py
  test/routes/
onb-msa-sp-inventories/
  contracts/openapi.yaml
  codegen/config.yaml
  api/generated/{models, interfaces}/
  api/generated/{routes, runtime}.py
  api/{models, routes, services, repositories}/
  api/{__init__, contract, errors, security, seed}.py
  test/routes/
codegen/templates/
codegen/README.md
scripts/{setup_local, verify, generate_apis, generate_auth}.py
requirements-codegen.txt
test/{test_contracts, test_setup, test_system}.py
.secrets/                         # local, generado y excluido de Git
README.md
```

La notación entre llaves abrevia nombres separados, no carpetas literales.
Cada aplicación incluye `app.py`, `config.py`, `requirements.txt`, `.env.example`,
`requirements-codegen.txt`, `.gitignore`, `api/generated/manifest.json` y pruebas
de correspondencia de rutas y generación en `test/`. Los paquetes tienen `__init__.py`.
Las carpetas con guiones son proyectos independientes: no se importan como paquetes
ni comparten repositorios. La pequeña integración contractual se incluye en cada app.

## Detener, reiniciar y retomar la práctica

Pulsa `Ctrl+C` en las cuatro terminales. Para empezar con datos iniciales coherentes,
reinicia Pedidos e Inventario; puedes dejar Auth y Gateway levantados si su
configuración no cambió. Reiniciar solo uno de los servicios reinicia solo su memoria.
La próxima vez reutiliza `.venv` y `.secrets`, levanta las cuatro apps y haz login.
Al cerrar Pedidos normalmente con `Ctrl+C`, se espera a las validaciones aceptadas;
puede tardar según sus timeouts y la cantidad en cola. Un cierre forzado no garantiza
que terminen. El resultado sigue viviendo solo en memoria y se pierde al salir.
Después de suspender Windows comprueba los health; no hay servicios instalados que
arranquen automáticamente. Las claves se cargan al iniciar, no por cada solicitud.

## Solución de problemas

| Problema | Acción |
|---|---|
| No existe `py` | Instala Python con el lanzador y abre una terminal nueva. |
| No existe `.venv\Scripts\python.exe` | Entra en la raíz y crea el entorno del paso 2. |
| `ModuleNotFoundError` | Usa el Python de `.venv` e instala `requirements-codegen.txt` de la raíz. |
| Falla la generación o faltan herramientas | Instala `requirements-codegen.txt` y comprueba `java -version`. |
| `--check` indica código generado desactualizado | Ejecuta `scripts/generate_apis.py`; adapta la implementación si cambiaron las firmas. La sincronización se comprueba con ese comando y las pruebas, no automáticamente al arrancar Flask. |
| Falta un archivo en `.secrets` | Ejecuta `scripts/setup_local.py` después de instalar dependencias. |
| 401 en gateway | Inicia sesión, renueva un token vencido y revisa el encabezado Bearer. |
| 403 con el cliente en Inventario | Es el permiso previsto; crea pedidos para solicitar descuentos indirectamente. |
| 404 al consultar un pedido ajeno | El cliente solo puede consultar los suyos. |
| 401 entre servicios | Revisa que coincida la clave interna; reinicia tras cambiar secretos. |
| `ERROR_VALIDACION` al crear | Revisa Gateway, Inventario, credencial de Pedidos y timeouts. |
| 502/504 al iniciar sesión | Comprueba Auth en el puerto 5003 y `AUTH_SERVICE_URL`. |
| Puerto ocupado | Detén la instancia anterior; no ejecutes dos copias de la misma app. |
| Swagger UI vacío | Comprueba Internet para su CDN y abre el contrato YAML directamente. |
| Las pruebas detectan puertos ocupados | Detén las cuatro apps manuales antes de la verificación global. |

Para identificar procesos que escuchan, sin cerrarlos:

```powershell
Get-NetTCPConnection -LocalPort 5000,5001,5002,5003 -State Listen -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

Los logs aparecen en las terminales de cada aplicación. No hace falta cargar datos
en una base de datos ni levantar otro componente de infraestructura.

## Limitaciones de la práctica

- Al reiniciar se pierden pedidos, stock modificado y descuentos registrados.
  Varias instancias tendrían memorias y locks distintos: usa un proceso por app.
- Un timeout o respuesta perdida deja un resultado incierto: Inventario podría
  haber descontado antes del fallo. No hay compensación ni recuperación automática.
- Las validaciones pendientes viven en la cola del proceso de Pedidos. No hay
  cola persistente, límite de pedidos en espera ni recuperación tras una caída.
  `VALIDATION_WORKERS` limita los trabajadores simultáneos, no la longitud de la cola.
- Los JWT vencen; no hay refresh tokens, revocación inmediata ni endpoint de logout.
  El gateway verifica localmente, por lo que un token válido no depende de que Auth
  siga disponible. El login sí necesita ese servicio.
- Las cuentas quemadas y el HTTP local con claves internas son una práctica educativa.
  No expongas estos puertos a Internet. Para un entorno real habría que proteger
  el transporte, aislar los servicios y administrar usuarios y secretos adecuadamente.
- No hay base de datos, ORM, Redis, contenedores, broker de mensajes ni frontend.
  Los archivos de claves son configuración, no persistencia de negocio.

## Otro material y referencias

Los fundamentos se conservan en la rama
[`programming_fundamentals`](https://github.com/keax-dev/coe-ing/tree/programming_fundamentals).
Referencias: [PyJWT](https://pyjwt.readthedocs.io/en/stable/api.html),
[Werkzeug](https://werkzeug.palletsprojects.com/en/stable/utils/) e
[integración Flask de openapi-core](https://python-openapi.org/openapi-core/docs/latest/integrations/flask/).
La ejecución en segundo plano usa
[`ThreadPoolExecutor` de Python](https://docs.python.org/3.14/library/concurrent.futures.html#threadpoolexecutor).
