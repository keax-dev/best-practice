# Buenas prácticas aplicadas al trabajo

## ¿Qué es BP?

Es una colección educativa por temas basada en los manuales revisados. Explica la
práctica una vez aunque aparezca en varios documentos. Incluye Python, Spring
Boot, Angular y SQL de PostgreSQL. No incluye React ni implementaciones .NET.

Los comentarios y la documentación están en español; los identificadores y los
mensajes de los programas están en inglés. Las convenciones internas se distinguen
de las prácticas generales y de las decisiones didácticas.

## Temas

| Orden | Bloque | Qué aprenderás |
|---|---|---|
| 01 | [Estándares de Python](01_python_standards/definition.md) | Convenciones para leer y escribir Python de forma consistente. |
| 02 | [Manejo de errores](02_error_handling/definition.md) | Cómo comunicar fallos sin ocultarlos ni perder su causa. |
| 03 | [Arquitectura y responsabilidades](03_architecture/definition.md) | Cómo separar el negocio, las herramientas y la entrada HTTP en Python y Spring Boot. |
| 04 | [Configuración y seguridad](04_configuration_and_security/definition.md) | Cómo recibir parámetros externos y proteger las credenciales. |
| 05 | [Logs y observabilidad](05_logging_and_observability/definition.md) | Cómo explicar lo que ocurre durante una operación sin revelar datos sensibles. |
| 06 | [Recursos y rendimiento](06_resources_and_performance/definition.md) | Cómo limitar el consumo de memoria, conexiones y trabajo concurrente. |
| 07 | [Pruebas](07_testing/definition.md) | Cómo verificar comportamiento, errores y contratos con resultados repetibles. |
| 08 | [Resiliencia](08_resilience/definition.md) | Cómo responder de forma controlada cuando una dependencia falla o tarda demasiado. |
| 09 | [SQL y PostgreSQL](09_database_practices/definition.md) | Cómo nombrar, consultar y proteger datos con ejemplos específicos de PostgreSQL. |
| 10 | [Angular](10_frontend_conventions/definition.md) | Cómo organizar componentes, servicios y navegación en Angular. No incluye React. |
| 11 | [Entrega y revisión](11_delivery_and_review/definition.md) | Cómo preparar cambios trazables y revisables antes de publicarlos. |
| 12 | [Desarrollo con IA](12_ai_development/definition.md) | Cómo reutilizar capacidades y definir límites y responsabilidades al usar agentes. |

Hay **63 subtemas**. Cada subtema tiene `definition.md`. Las prácticas
Python usan `before.py` y `after.py` o un `example.py` completo. Las prácticas de
PostgreSQL usan `before.sql` y `after.sql`. Angular tiene fragmentos compilables
con pruebas y Spring Boot una aplicación mínima independiente. Entrega e IA usan
casos `before.md` y `after.md`: no ejecutan despliegues, correos ni aprobaciones.

## Preparación de Python

Desde la raíz `coe-ing`, usando PowerShell:

```powershell
py -3.14 --version
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\BP\requirements-lock.txt
```

El entorno objetivo es Python 3.14.7. Usa el ejecutable de `.venv` después de
instalar dependencias: `py -3.14` selecciona el Python global y puede no encontrar
los paquetes del entorno. No copies `.venv` de otra máquina.

`requirements.txt` declara las herramientas principales y `requirements-lock.txt`
fija también sus dependencias para reproducir el entorno verificado. Los ejemplos
SQL y Angular tienen sus propios `package-lock.json` para usar `npm ci`.

Ejecutar una comparación y después todas las demostraciones:

```powershell
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\03_exception_chaining\before.py
.\.venv\Scripts\python.exe -B .\BP\02_error_handling\03_exception_chaining\after.py
.\.venv\Scripts\python.exe -B .\BP\run_examples.py
```

El ejecutor usa procesos independientes y no levanta servidores. Ejecutar una
demostración no reemplaza una prueba: los before muestran problemas intencionales
y algunos imprimen un resultado diferente al after. Los logs pueden salir por
stderr sin que el proceso haya fallado.

## Pruebas Python

Desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m pytest -c BP/pytest.ini -q
.\.venv\Scripts\python.exe -B .\BP\check_materials.py
.\.venv\Scripts\python.exe -m ruff check BP --config BP/pyproject.toml --no-cache
```

Para medir la lección de cobertura, sin confundirla con toda la colección:

```powershell
.\.venv\Scripts\python.exe -m pytest -c BP/pytest.ini BP/07_testing/08_code_coverage --cov=BP/07_testing/08_code_coverage --cov-branch --cov-config=BP/.coveragerc --cov-report=term-missing --cov-fail-under=75
```

El 75 % de ese comando es un umbral didáctico explícito. No certifica el porcentaje
que corresponde exigir a cada stack corporativo. La lección de mutación simula un
mutante concreto; no se presenta como una herramienta completa de mutación.

## Flask

El ejemplo de arquitectura se prueba con el mismo comando pytest. Si quieres
abrirlo por HTTP, desde la raíz puedes usar una terminal dedicada:

```powershell
Set-Location .\BP\03_architecture\04_flask_application_structure
..\..\..\.venv\Scripts\python.exe -m flask --app api:create_app run --host 127.0.0.1 --port 5010 --no-reload
```

En otra terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:5010/orders
Invoke-RestMethod http://127.0.0.1:5010/orders -Method Post -ContentType application/json -Body '{"quantity":2}'
```

Detén el servidor con Ctrl+C. El estado se pierde al reiniciar y su capacidad está
limitada a 100 pedidos. Es una práctica local sin autenticación.

## Spring Boot

Necesitas JDK 21 y Maven 3.9 o posterior en PATH. Compruébalos con `java -version`
y `mvn -version`. El ejemplo fija Spring Boot 3.5.16 y no necesita una base de datos.
Si falta Maven, instálalo siguiendo la [guía oficial](https://maven.apache.org/install.html)
y abre una terminal nueva para que se actualice PATH.
Desde la raíz, en una terminal nueva:

```powershell
Set-Location .\BP\03_architecture\05_spring_boot_structure
mvn test
mvn spring-boot:run
```

En otra terminal, prueba las rutas:

```powershell
Invoke-RestMethod http://127.0.0.1:5011/orders
Invoke-RestMethod http://127.0.0.1:5011/orders -Method Post -ContentType application/json -Body '{"quantity":2}'
Invoke-RestMethod http://127.0.0.1:5011/actuator/health/liveness
Invoke-RestMethod http://127.0.0.1:5011/actuator/health/readiness
```

El puerto puede cambiarse con APP_PORT antes de arrancar. Las pruebas HTTP usan
un puerto aleatorio; no necesitan otro servidor levantado. El reporte de cobertura
queda en `target/site/jacoco/index.html` después de `mvn test`. El ejemplo no incluye
JWT ni persistencia: muestra arquitectura, validación y pruebas.

## Angular

Necesitas Node compatible con Angular 21 (por ejemplo, Node 24). En una terminal
nueva desde la raíz:

```powershell
Set-Location .\BP\10_frontend_conventions
npm ci
npm test
```

Se fijan Angular 21.2.26 y TypeScript 5.9.3. `npm test` compila los componentes y
plantillas con el compilador de Angular y ejecuta pruebas de inyección, guard e
interceptor. No abre un navegador. Son ejemplos compilables para estudiar, no una
aplicación con `npm start` ni un reemplazo del frontend que ya construimos.

## PostgreSQL sin instalar un servidor

Desde la raíz, en otra terminal:

```powershell
Set-Location .\BP\09_database_practices
npm ci
npm test
```

PGlite ejecuta un motor PostgreSQL embebido en memoria. No sustituye SQL con SQLite
ni requiere Docker o un servidor de base de datos. Ejecuta ambos scripts de cada
lección, comprueba sus resultados y cierra la instancia. Cada script utiliza una
transacción y tablas temporales, y termina con ROLLBACK.

Si ya tienes PostgreSQL, también puedes abrir un script con `psql` sobre una base
de práctica. Los planes del motor embebido no certifican rendimiento de producción.

## Relación con lo que ya existe

- [SOLID](../solid/README.md) mantiene las definiciones de sus cinco principios.
- [Clean Code](../clean_code/README.md) mantiene los ejemplos de legibilidad.
- BP explica su aplicación y enlaza esas carpetas cuando corresponde.
- [SOURCES.md](SOURCES.md) identifica el origen de los temas.
- [CLARIFICATIONS.md](CLARIFICATIONS.md) registra ambigüedades y adaptaciones.

No se requieren conexiones al banco, librerías privadas ni datos reales. Las
versiones de este ejercicio no equivalen a aprobación del catálogo corporativo.
