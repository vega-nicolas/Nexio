async function verificarToken() {
    const token = sessionStorage.getItem("access_token");
    
    if (!token) {
        window.location.href = "/login";
        return;
    }

    try {
        const response = await fetch("/api/protected/", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if (!response.ok) {
            window.location.href = "/login";
        }

    } catch (error) {
        console.error("Error verificando el token:", error);
        window.location.href = "/login";
    }
}