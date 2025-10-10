document.getElementById('form-empleado').addEventListener('submit', function (e) {
  e.preventDefault();
  agregarEmpleado();
});

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

agregarEmpleado = async () => 
  {
    const nombres = document.querySelector('input[name="nombres"]').value;
    const apellidos = document.querySelector('input[name="apellidos"]').value;
    const rut = document.querySelector('input[name="rut"]').value;
    const fecha_nacimiento = document.querySelector('input[name="fecha_nacimiento"]').value;
    const direccion = document.querySelector('input[name="direccion"]').value;
    const empresa_id = parseInt(document.querySelector('select[name="empresa_id"]').value);
    const afp_id = parseInt(document.querySelector('select[name="afp_id"]').value);
    const salud_id = parseInt(document.querySelector('select[name="salud_id"]').value);
    const afc_id = parseInt(document.querySelector('select[name="afc_id"]').value);
    const fecha_inicio = document.querySelector('input[name="fecha_ingreso"]').value;
    const sueldo_base = parseInt(document.querySelector('input[name="sueldo_base"]').value);
    const tipo_contrato = afc_id === 1 ? "INDEFINIDO" : "PLAZO FIJO";
    const fecha_termino = null;

    const nuevoEmpleado = {
      nombres,
      apellidos,
      rut,
      fecha_nacimiento,
      direccion,
      empresa_id,
      tipo_contrato,
      fecha_inicio,
      fecha_termino,
      sueldo_base,
      afp_id,
      salud_id,
      afc_id
    };

    console.log('Nuevo Empleado:', nuevoEmpleado);

    const respuesta = await consumirAPI('api/v1/empleados', 'POST', nuevoEmpleado);
    console.log('Empleado agregado:', respuesta);
  }