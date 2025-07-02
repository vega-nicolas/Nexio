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
            showMessage('Username cannot exceed 30 characters', 'error');
            alert('Error: Username cannot exceed 30 characters');
            return;
        }
        if (data.password.length < 12) {
            showMessage('Password must be at least 12 characters long', 'error');
            alert('Error: Password must be at least 12 characters');
            return;
        }

        if (document.querySelector('input[name="password"]').value !== document.querySelector('input[name="confirmPassword"]').value) {
            showMessage('Passwords must match', 'error');
            alert("Passwords must match");
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

            if (response.status === 201) {
                form.reset();
                window.location.href = '/login';
            } else if (response.status === 409) {
                showMessage(result.detail || 'Email or username is already registered.', 'error');
                alert(`Error: ${result.detail || 'Email or username is already registered.'}`);
            } else if (response.status === 500) {
                showMessage(result.detail || 'Internal server error. Please try again.', 'error');
                alert(`Error: ${result.detail || 'Internal server error. Please try again.'}`);
            } else {
                showMessage(result.detail || 'Registration failed. Please try again.', 'error');
                alert(`Error: ${result.detail || 'Registration failed. Please try again.'}`);
            }
        } catch (error) {
            showMessage('Connection error. Please check your network and try again.', 'error');
            alert('Connection error: Please check your network and try again.');
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