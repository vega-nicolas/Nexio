async function verificarToken() {
    const token = localStorage.getItem("access_token");
    
    if (token != null) {

        try {
            const response = await fetch("/api/validtoken/", {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + token
                }
            });
    
            if (response.ok) {
                // Valid Token
                document.getElementById('login').remove();
                document.getElementById('register').remove();
            }
    
        } catch (error) {
            console.error("Error verificando el token:", error);
            
        }
    }

}
document.addEventListener("DOMContentLoaded", verificarToken);