async function consumirAPI(url, metodo = 'GET', datos = null) {
  try {
    const opciones = {
      method: metodo,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (datos) {
      opciones.body = JSON.stringify(datos);
    }

    const response = await fetch(url, opciones);

    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('Respuesta:', data);
    return data;

  } catch (error) {
    console.error('Error al consumir el API:', error);
  }
}
