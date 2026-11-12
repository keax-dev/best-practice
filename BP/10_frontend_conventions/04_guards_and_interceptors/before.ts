// Tema: comprobar solo si se muestra un botón no protege una ruta ni la API.
export function showOrdersButton(hasSession: boolean): boolean {
  return hasSession;
}
