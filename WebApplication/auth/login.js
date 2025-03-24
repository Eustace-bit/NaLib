document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error("Login failed");
        }

        const result = await response.json();
        sessionStorage.setItem("access_token", JSON.stringify(result.access_token));
        sessionStorage.setItem("userRole", result.role || "user"); // Store user role

        // Redirect to index.html on successful login
        window.location.href = "../system/index.html";
    } catch (error) {
        // Display error message
        document.getElementById("result").innerText = "Login failed. Please check your credentials.";
        console.error("Login error:", error);
    }
});