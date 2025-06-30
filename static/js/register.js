document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('registerForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = {
            email: formData.get('email'),
            username: formData.get('username'),
            displayName: formData.get('displayName'),
            password: formData.get('password')
        };

        if (data.username.length > 30) {
            showMessage('El nombre de usuario no puede exceder 30 caracteres', 'error');
            alert('Error: El nombre de usuario no puede exceder 30 caracteres');
            return;
        }
        if (data.password.length < 8) {
            showMessage('La contraseña debe tener al menos 8 caracteres', 'error');
            alert('Error: La contraseña debe tener al menos 8 caracteres');
            return;
        }

        if (document.querySelector('input[name="password"]').value !== document.querySelector('input[name="confirmPassword"]').value){
            showMessage('Las contraseñas deben ser idénticas', 'error');
            alert("Las contraseñas deben ser idénticas");
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/adduser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Manejar códigos de estado HTTP
            if (response.status === 201) {
                form.reset();
                window.location.href = '/login';
            } else if (response.status === 409) {
                showMessage(result.detail || 'El email o nombre de usuario ya está registrado.', 'error');
                alert(`Error: ${result.detail || 'El email o nombre de usuario ya está registrado.'}`);
            } else if (response.status === 500) {
                showMessage(result.detail || 'Error interno del servidor. Intenta de nuevo.', 'error');
                alert(`Error: ${result.detail || 'Error interno del servidor. Intenta de nuevo.'}`);
            } else {
                showMessage(result.detail || 'Error al registrarse. Intenta de nuevo.', 'error');
                alert(`Error: ${result.detail || 'Error al registrarse. Intenta de nuevo.'}`);
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
        responseMessage.className = `mt-4 ${type}`;
        responseMessage.classList.remove('hidden');
        setTimeout(() => {
            responseMessage.classList.add('hidden');
        }, 5000);
    }
});