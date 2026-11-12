# Aplicación Flask por responsabilidades

## ¿Qué es?

Es distribuir la entrada HTTP, el negocio y el almacenamiento en archivos con una función clara.

## ¿Cómo funciona y para qué sirve?

create_app compone un repositorio y un servicio por aplicación. Blueprint registra una MethodView con métodos de instancia y as_view.

## Qué muestra el ejemplo

example.py realiza un POST en memoria. api/models.py representa el dato, service.py lo crea, repository.py guarda y routes.py traduce HTTP. test_example.py prueba esa composición.

Tecnología: **Python y Flask**.

## Cómo revisarlo o ejecutarlo

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B .\BP\03_architecture\04_flask_application_structure\example.py
.\.venv\Scripts\python.exe -m pytest -c BP/pytest.ini BP/03_architecture/04_flask_application_structure -q
```

## Qué pide la organización

La guía interna pide aplicar esta práctica según el tipo de componente. Los valores del ejemplo son didácticos y no representan parámetros productivos aprobados.

## Límites y aclaraciones

El almacenamiento es local y limitado a 100 pedidos de demostración. No es persistencia ni una API productiva. No incluye autenticación ni todo el ejercicio de microservicios.

## Referencias

Consulta [general](../../SOURCES.md#general) para identificar el manual de origen.
Las precisiones pendientes se registran en [CLARIFICATIONS.md](../../CLARIFICATIONS.md).
