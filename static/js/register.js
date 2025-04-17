document.addEventListener('DOMContentLoaded', () => {
    // Detectar preferencia inicial del sistema
    function setTheme(theme) {
        const body = document.body;
        const themeIcon = document.getElementById('themeIcon');
        
        if (theme === 'system') {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            body.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        } else {
            body.setAttribute('data-theme', theme);
        }

        // Actualizar ícono
        if (body.getAttribute('data-theme') === 'dark') {
            themeIcon.innerHTML = `
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z">
                </path>`;
        } else {
            themeIcon.innerHTML = `
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z">
                </path>`;
        }

        localStorage.setItem('theme', theme);
    }

    // Aplicar tema inicial
    const savedTheme = localStorage.getItem('theme') || 'system';
    setTheme(savedTheme);

    // Alternar tema al hacer clic
    document.getElementById('themeToggle').addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    // Escuchar cambios en la preferencia del sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (document.body.getAttribute('data-theme') === 'system') {
            setTheme('system');
        }
    });

    // Manejo del formulario
    document.getElementById('registerForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;
        const responseMessage = document.getElementById('responseMessage');
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

        if (document.querySelector('input[name="password"]').value != document.querySelector('input[name="confirmPassword"]').value){
            showMessage('Las contraseñas deben ser identicas', 'error');
            alert("Las contraseñas deben ser identicas")
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
                showMessage('Registro exitoso. ¡Bienvenido a Nexio!', 'success');
                alert('¡Registro exitoso! Bienvenido a Nexio');
                form.reset();
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