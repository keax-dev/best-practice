# Manejo de caché con Python

Una caché guarda una copia de datos o resultados para evitar repetir trabajo.
El **origen** sigue siendo la fuente de verdad: una caché puede expirar, vaciarse
o contener información desactualizada.

Los ejemplos son independientes, usan solamente la biblioteca estándar y se
verifican con **Python 3.14.7**. Cada carpeta contiene `definition.md` y `example.py`.
El código usa nombres y mensajes en inglés; la explicación y los comentarios
están en español.

## Preparación y ejecución

Abre PowerShell en el repositorio:

```powershell
cd C:\Users\jimen\Documents\coe-ing
py -3.14 --version
py -3.14 .\01_cache_basics\example.py
```

No necesitas instalar dependencias, iniciar servidores ni crear un entorno virtual.
Lee la definición, ejecuta el ejemplo y compara el resultado con lo explicado.
Cada ejecución empieza con memoria nueva y termina por sí sola.

| Orden | Tema | Qué observar |
|---|---|---|
| 1 | [Fundamentos](01_cache_basics/definition.md) | Hit, miss y consultas al origen |
| 2 | [Memoización](02_memoization/definition.md) | Resultados reutilizados según argumentos |
| 3 | [TTL](03_expiration_ttl/definition.md) | Caducidad desde la escritura |
| 4 | [LRU](04_eviction_lru/definition.md) | Expulsión por falta de capacidad |
| 5 | [Cache-aside](05_cache_aside/definition.md) | Cargar solamente cuando falta un dato |
| 6 | [Invalidación](06_invalidation/definition.md) | Refrescar un precio después de modificarlo |
| 7 | [Concurrencia](07_concurrent_access/definition.md) | Varias consultas comparten una carga |
| 8 | [Métricas](08_cache_metrics/definition.md) | Hits, misses y proporción de aciertos |

Para ejecutar todos:

```powershell
Get-ChildItem -Directory -Filter '0*' | Sort-Object Name | ForEach-Object {
    py -3.14 (Join-Path $_.FullName 'example.py')
    if ($LASTEXITCODE -ne 0) { throw "Example failed: $($_.Name)" }
}
```

## Cómo se combinan las estrategias

**Cache-aside** decide cómo cargar datos, **TTL** cuánto tiempo son válidos,
**LRU** qué expulsar al llenarse y la **invalidación** cómo retirar una copia
cuando cambia el origen. Pueden utilizarse juntas. Memoizar es guardar resultados
de funciones; `lru_cache` añade un límite de entradas, pero no TTL.

Para un catálogo: usar el ID como clave, buscar primero en caché, cargar en un
miss, caducar según la frescura aceptable e invalidar tras cambiar un precio.
Para confirmar una compra, comprobar precio y disponibilidad en el origen.
Si los datos dependen de usuario, idioma o permisos, esa diferencia debe reflejarse
en la clave; autoriza el acceso antes de devolver datos almacenados.

Los ejemplos aíslan cada concepto: no forman una caché completa de producción.
Los diccionarios sencillos no tienen límites ni sincronización salvo cuando la
lección los añade. La memoria no se comparte entre procesos o equipos y se pierde
al terminar. Un TTL no limita por sí solo el consumo de memoria ni garantiza
frescura inmediata. La caché tampoco debe ser el único lugar donde guardar pedidos.

## Pruebas

```powershell
py -3.14 -B -m unittest discover -s tests -v
```

Las pruebas verifican caducidad con un reloj controlado, expulsión, invalidación,
fallos del origen y carga concurrente. Los tiempos impresos son ilustrativos:
no se afirma una aceleración fija ni se prueba comparando milisegundos.

## Referencias

- [Python: functools](https://docs.python.org/3.14/library/functools.html).
- [Python: reloj monotónico](https://docs.python.org/3.14/library/time.html#time.monotonic).
- [Microsoft: patrón cache-aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).
- [Python: locks e hilos](https://docs.python.org/3.14/library/threading.html).
