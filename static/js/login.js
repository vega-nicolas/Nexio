document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('loginForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = new URLSearchParams();
        data.append('username', formData.get('email'));
        data.append('password', formData.get('password'));

        if (formData.get('password').length < 8) {
            showMessage('Password must be at least 8 characters long', 'error');
            alert('Error: Password must be at least 8 characters');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: data,
            });

            const result = await response.json();

            if (response.status === 202) {
                localStorage.setItem('access_token', result.access_token);
                form.reset();
                window.location.href = '/';
            } else if (response.status === 401) {
                showMessage(result.detail || 'Invalid credentials.', 'error');
                alert(`Error: ${result.detail || 'Invalid credentials.'}`);
            } else {
                showMessage(result.detail || 'Login failed. Please try again.', 'error');
                alert(`Error: ${result.detail || 'Login failed. Please try again.'}`);
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
        responseMessage.className = `mt-4 ${type === 'error' ? 'text-red-500' : 'text-green-500'}`;
        responseMessage.classList.remove('hidden');
        setTimeout(() => {
            responseMessage.classList.add('hidden');
        }, 5000);
    }
});

async function isTokenValid() {
    const token = sessionStorage.getItem("access_token");
    if (!token) return false;
    try {
        const response = await fetch("/api/validtoken/", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        });
        return response.ok;
    } catch (error) {
        console.error("Error verifying token:", error);
        return false;
    }
}