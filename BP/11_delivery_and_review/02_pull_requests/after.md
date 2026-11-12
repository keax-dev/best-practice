# PR mejorado
Título: Rechazar cantidades no positivas al crear pedidos.

Historia: DEMO-101. La API rechazaba cero demasiado tarde; ahora devuelve 400 antes de guardar. Se verificaron cero, negativos, booleanos y el caso válido. No cambia el contrato de respuestas exitosas.
