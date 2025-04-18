document.addEventListener('DOMContentLoaded', () => {
    // Manejo del formulario
    document.getElementById('registerForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = new URLSearchParams();
        data.append('username', formData.get('email'));
        data.append('password', formData.get('password'));

        // Validaciones

        if (formData.get('password').length < 8) {
            showMessage('La contraseña debe tener al menos 8 caracteres', 'error');
            alert('Error: La contraseña debe tener al menos 8 caracteres');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/validuser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: data,
            });

            const result = await response.json();

            // Manejar códigos de estado HTTP
            if (response.status === 202) {
                showMessage('Login exitoso', 'success');
                alert('Login exitoso! Bienvenido a Nexio');
                form.reset();
                window.location.href = '/';
            } else if (response.status === 401) {
                showMessage(result.detail || 'Credenciales inválidas.', 'error');
                alert(`Error: ${result.detail || 'Credenciales inválidas.'}`);
            } else {
                showMessage(result.detail || 'Error al iniciar sesión. Intenta de nuevo.', 'error');
                alert(`Error: ${result.detail || 'Error al iniciar sesión. Intenta de nuevo.'}`);
            }
        } catch (error) {
            showMessage('Error de conexión. Verifica tu red e intenta de nuevo.', 'error');
            alert('Error de conexión: Verifica tu red e intenta de nuevo.');
            console.error('Error:', error);
        }
    });

    function showMessage(message, type) {
        const responseMessage = document.getElementById('responseMessage');
        responseMessage.textContent = message;
        responseMessage.className = `mt-4 ${type === 'error' ? 'text-red-500' : 'text-green-500'}`;
        responseMessage.classList.remove('hidden');
        setTimeout(() => {
            responseMessage.classList.add('hidden');
        }, 5000);
    }
});