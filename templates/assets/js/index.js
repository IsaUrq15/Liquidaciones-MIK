export async function consumirAPI(url, metodo = 'GET', datos = null) {
  try {
    const opciones = {
      method: metodo,
      headers: { 'Content-Type': 'application/json' }
    };

    if (datos) opciones.body = JSON.stringify(datos);

    const response = await fetch(url, opciones);

    // Siempre intenta parsear JSON, aunque haya error HTTP
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      // Devuelve el detalle del backend si existe
      return data || { detail: `Error HTTP ${response.status}` };
    }

    console.log('Respuesta:', data);
    return data;

  } catch (error) {
    console.error('Error al consumir el API:', error);
    // Devolver algo manejable también en errores de red
    return { detail: 'Error de conexión con el servidor' };
  }
}
