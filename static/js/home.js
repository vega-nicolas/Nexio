async function verifyToken() {
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
                // Valid token
                document.getElementById('login').remove();
                document.getElementById('register').remove();
            }

        } catch (error) {
            console.error("Error verifying token:", error);
        }
    }
}

document.addEventListener("DOMContentLoaded", verifyToken);