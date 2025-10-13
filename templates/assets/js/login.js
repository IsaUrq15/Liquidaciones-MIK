import { consumirAPI } from './index.js';

async function login() {
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const datos = { email, password };
    const url = 'http://localhost:8000/api/v1/usuarios/login';

    try {
        const respuesta = await consumirAPI(url, 'POST', datos);
        console.log('Respuesta del login:', respuesta);

        if (respuesta?.message) {
            localStorage.setItem('message', respuesta.message);
            window.location.href = 'home';
        } else {
            console.error('Error del login:', respuesta);
            alert(respuesta?.detail || 'Error en el login. Verifica tus credenciales.');
        }
    } catch (error) {
        console.error('Excepción en login:', error);
        alert('Error de conexión o respuesta inválida del servidor.');
    }
}

window.login = login;