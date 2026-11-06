# Auth: API first con generación de código

Auth, Pedidos, Inventario y Gateway utilizan generación desde sus contratos OpenAPI.
La [guía compartida](../codegen/README.md) explica el generador y el
[README principal](../README.md) detalla instalación, claves, permisos y arranque completo.

## Archivos generados y código manual

```text
contracts/openapi.yaml
api/generated/
  models/
    login_input.py          # LoginInput y LoginInputSchema
    token.py                # Token y TokenSchema
    health.py               # Health y HealthSchema
    error.py                # Error y ErrorSchema
  interfaces/auth_api.py    # AuthAPI abstracta
  routes.py                 # Blueprint, MethodView y registro de operaciones
  runtime.py                # Utilidades de serialización generadas
  manifest.json             # Huella de entradas y archivos generados
api/routes/auth.py           # AuthAPIImpl manual
api/services/auth.py         # Credenciales y emisión de JWT
api/repositories/user.py     # Usuarios locales
api/models/user.py           # Modelo de negocio
```

La ruta generada convierte el JSON en `LoginInput`, llama a `AuthAPIImpl.login()`
y serializa el `Token` devuelto. `AuthAPIImpl` hereda de `AuthAPI`, que exige
`login()` y `get_health()`. `ContractView` valida solicitudes y respuestas contra
OpenAPI durante la ejecución. `/docs` y `/openapi.yaml` quedan fuera de esa validación.

No edites `api/generated/`: se regenera y se incluye en Git. No hay esquemas HTTP
manuales duplicados. Los servicios y repositorios siguen siendo manuales y no se
sobrescriben al generar.

## Instalación y generación

Desde la raíz `coe-ing`, con el entorno virtual creado según el README principal
y Java 21 disponible en PATH:

```powershell
java -version
.\.venv\Scripts\python.exe -m pip install -r .\requirements-codegen.txt
.\.venv\Scripts\python.exe scripts\setup_local.py

# Generar y comprobar únicamente Auth.
.\.venv\Scripts\python.exe scripts\generate_apis.py --app auth
.\.venv\Scripts\python.exe scripts\generate_apis.py --app auth --check

# Generar y comprobar todo el ejercicio.
.\.venv\Scripts\python.exe scripts\generate_apis.py
.\.venv\Scripts\python.exe scripts\generate_apis.py --check
```

`scripts/generate_auth.py` sigue disponible como comando compatible para Auth.
Las plantillas compartidas están en `codegen/templates/` en la raíz del repositorio;
la configuración de Auth está en `onb-msa-sp-auth/codegen/config.yaml`.
El JAR se instala con el paquete Python; no requiere Docker ni Node.js.
Java y el generador solo son necesarios para regenerar y ejecutar las pruebas de
generación, no para arrancar Flask con los archivos existentes.

## Flujo al modificar la API

1. Edita el contrato, incluidas las restricciones y ejemplos.
2. Ejecuta `scripts/generate_apis.py --app auth`.
3. Adapta `AuthAPIImpl` si cambiaste las firmas de la interfaz.
4. Implementa el comportamiento y actualiza las pruebas necesarias.
5. Ejecuta la comprobación `--check` y las pruebas.
6. Revisa juntos contrato, artefactos e implementación.

La comprobación genera en una carpeta temporal y detecta diferencias sin
sobrescribir archivos. Las diferencias LF/CRLF no causan cambios falsos.
Si una construcción OpenAPI todavía no está soportada, el generador falla antes
de publicar: consulta el alcance de las plantillas en la guía compartida.
Reinicia Auth después de regenerar si estaba levantado.

## Ejecutar y probar

```powershell
# Arrancar Auth, puerto 5003, desde la raíz del repositorio.
.\.venv\Scripts\python.exe .\onb-msa-sp-auth\app.py
```

En otra terminal desde la raíz:

```powershell
Push-Location .\onb-msa-sp-auth
..\.venv\Scripts\python.exe -m pytest test -v
Pop-Location
```

La suite comprueba DTO tipados, interfaz obligatoria, restricciones generadas,
reproducibilidad, detección de cambios y conservación de archivos manuales.
Para comprobar todo el ejercicio, detén los servidores locales y ejecuta:

```powershell
.\.venv\Scripts\python.exe scripts\verify.py
```

Documentación: `http://127.0.0.1:5003/docs`.
Contrato: `http://127.0.0.1:5003/openapi.yaml`.
