function toggleRegister() {
  const box = document.getElementById("register-box");
  box.style.display = box.style.display === "none" ? "block" : "none";
}

async function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  try {
    const data = await apiRequest("/auth/login", "POST", { email, password }, false);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("username", data.username);
    document.getElementById("auth-message").innerText = `Welcome, ${data.username}!`;
    document.getElementById("auth-link").innerText = data.username;
  } catch (e) {
    document.getElementById("auth-message").innerText = e.message;
  }
}

async function register() {
  const username = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;
  try {
    await apiRequest("/auth/register", "POST", { username, email, password }, false);
    document.getElementById("auth-message").innerText = "Registered! Please login.";
  } catch (e) {
    document.getElementById("auth-message").innerText = e.message;
  }
}
