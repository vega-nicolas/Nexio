document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");
    let offset = 0;
    const pageSize = 10;
    let isLoading = false;
    let lastScrollY = window.scrollY; // Track last scroll position

    // Verify token
    async function verifyToken() {
        if (!token) return false;

        try {
            const response = await fetch("/api/validtoken/", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (response.ok) {
                document.getElementById('login')?.remove();
                document.getElementById('register')?.remove();
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error("Token verification error:", error);
            return false;
        }
    }

    // Handle post submission
    async function handlePostSubmit(e) {
        e.preventDefault();

        const textarea = document.getElementById("textpost");
        const postText = textarea.value.trim();

        if (!token) {
            alert("You are not authenticated.");
            return window.location.href = "/login";
        }

        if (!postText) {
            alert("Post content cannot be empty.");
            return;
        }

        const isValid = await verifyToken();
        if (!isValid) {
            alert("Invalid token. Please log in again.");
            return window.location.href = "/login";
        }

        try {
            const response = await fetch("/api/post/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ text: postText })
            });

            if (response.status === 201) {
                alert("Post published successfully!");
                textarea.value = "";
                offset = 0; // Reset offset
                await loadPosts(0, false); // Reload all posts
            } else {
                alert("Error while publishing the post.");
            }
        } catch (error) {
            console.error("Error submitting post:", error);
        }
    }

    // Load posts
    async function loadPosts(start = 0, append = false) {
        if (isLoading) return;
        isLoading = true;

        try {
            const response = await fetch(`/api/getpost/${start}/`);
            const posts = await response.json();

            if (!posts.length) {
                console.log("No more posts to load.");
                return;
            }

            let html = "";

            for (let i = 0; i < posts.length; i++) {
                const post = posts[i];
                html += `
                    <div class="post">
                        <div class="post-header">
                            <strong>${post.display_name}</strong> <span>@${post.preferred_username}</span>
                            <span class="post-date">${new Date(post.created_at).toLocaleString('en-GB', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false
                })}</span>
                        </div>
                        <div class="post-body">
                            <p>${post.text}</p>
                        </div>
                        <div class="post-footer">
                            <span>👍 ${post.likes} Likes</span>
                            <span>💬 ${post.comments} Comments</span>
                            <span>🔁 ${post.shares} Shares</span>
                        </div>
                    </div>
                `;
            }

            const container = document.getElementById("allpost");
            if (append) {
                container.innerHTML += html;
            } else {
                container.innerHTML = html;
            }

            offset += pageSize;
        } catch (error) {
            console.error("Error loading posts:", error);
        } finally {
            isLoading = false;
        }
    }

    // Scroll handling for infinite scroll and postdiv visibility
    window.addEventListener("scroll", () => {
        const currentScrollY = window.scrollY;
        const postDiv = document.querySelector(".postdiv");

        // Toggle postdiv visibility based on scroll direction
        if (currentScrollY > lastScrollY && currentScrollY > 50) {
            // Scrolling down and past 50px
            postDiv.classList.add("hidden");
        } else {
            // Scrolling up or near top
            postDiv.classList.remove("hidden");
        }
        lastScrollY = currentScrollY;

        // Infinite scroll for posts
        const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
        if (nearBottom && !isLoading) {
            loadPosts(offset, true); // append = true
        }
    });

    // Init
    await verifyToken();
    await loadPosts(offset);

    // Post form submit
    const form = document.getElementById("postform");
    if (form) {
        form.addEventListener("submit", handlePostSubmit);
    }
});