document.addEventListener("DOMContentLoaded", function() {
    const loginTab = document.getElementById("login-tab");
    const registerTab = document.getElementById("register-tab");
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");

    loginTab.addEventListener("click", function() {
        loginTab.classList.add("active");
        registerTab.classList.remove("active");
        loginForm.classList.remove("hidden");
        registerForm.classList.add("hidden");
    });

    registerTab.addEventListener("click", function() {
        registerTab.classList.add("active");
        loginTab.classList.remove("active");
        registerForm.classList.remove("hidden");
        loginForm.classList.add("hidden");
    });

    // ✅ Handle Login
    document.querySelector("#login-form form").addEventListener("submit", async function(event) {
        event.preventDefault();
        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        const response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Login Successful!");
            window.location.href = "index.html"; // Redirect to dashboard
        } else {
            alert(data.error);
        }
    });

    // ✅ Handle Register
    document.querySelector("#register-form form").addEventListener("submit", async function(event) {
        event.preventDefault();
        const name = document.getElementById("name").value;
        const email = document.getElementById("register-email").value;
        const password = document.getElementById("register-password").value;

        const response = await fetch("/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Registration Successful! Please log in.");
            loginTab.click(); // Switch to login tab
        } else {
            alert(data.error);
        }
    });
});
