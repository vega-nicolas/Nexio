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
});