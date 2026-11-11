const AUTH_API_URL = "http://127.0.0.1:8000";

console.log("✅ auth.js se načetl");

/* =====================================
   REGISTRACE
===================================== */

const registerForm = document.getElementById("registerForm");

if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    console.log("🟢 REGISTRACE BYLA ODESLÁNA");

    const name = document.getElementById("registerName").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;
    const passwordConfirm = document.getElementById(
      "registerPasswordConfirm",
    ).value;

    const message = document.getElementById("registerMessage");

    message.textContent = "";

    if (!name || !email || !password || !passwordConfirm) {
      message.textContent = "⚠️ Vyplň všechna pole.";
      return;
    }

    if (password.length < 6) {
      message.textContent = "⚠️ Heslo musí mít alespoň 6 znaků.";
      return;
    }

    if (password !== passwordConfirm) {
      message.textContent = "⚠️ Hesla se neshodují.";
      return;
    }

    message.textContent = "🤖 Vytvářím účet...";

    try {
      const response = await fetch(AUTH_API_URL + "/auth/register", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          name: name,
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registrace se nepodařila.");
      }

      message.textContent =
        "✅ Registrace proběhla úspěšně. Za chvíli budete přesměrováni na přihlášení.";

      setTimeout(() => {
        window.location.href = "login.html";
      }, 3000);
    } catch (error) {
      console.error("Registrace selhala:", error);

      message.textContent = "❌ " + error.message;
    }
  });
}

/* =====================================
   PŘIHLÁŠENÍ
===================================== */

const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    const message = document.getElementById("loginMessage");

    message.textContent = "";

    if (!email || !password) {
      message.textContent = "⚠️ Vyplň e-mail a heslo.";
      return;
    }

    message.textContent = "🤖 Přihlašuji...";

    try {
      const response = await fetch(AUTH_API_URL + "/auth/login", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        let errorMessage = "Přihlášení se nepodařilo.";

        if (typeof data.detail === "string") {
          errorMessage = data.detail;
        } else if (Array.isArray(data.detail)) {
          errorMessage = data.detail.map((error) => error.msg).join(", ");
        }

        throw new Error(errorMessage);
      }

      localStorage.setItem("access_token", data.access_token);

      localStorage.setItem("user_name", data.user.name);

      message.textContent = "✅ Přihlášení proběhlo úspěšně.";

      setTimeout(() => {
        window.location.href = "index.html";
      }, 800);
    } catch (error) {
      console.error("Přihlášení selhalo:", error);

      message.textContent = "❌ " + error.message;
    }
  });
}

/* =====================================
   ODHLÁŠENÍ
===================================== */

document.addEventListener("DOMContentLoaded", () => {
  const logoutMenuLink = document.getElementById("logoutMenuLink");
  const loginMenuLink = document.getElementById("loginMenuLink");
  const registerMenuLink = document.getElementById("registerMenuLink");

  if (!logoutMenuLink) {
    return;
  }

  const token = localStorage.getItem("access_token");

  if (token) {
    logoutMenuLink.style.display = "block";

    if (loginMenuLink) {
      loginMenuLink.style.display = "none";
    }

    if (registerMenuLink) {
      registerMenuLink.style.display = "none";
    }
  }

  logoutMenuLink.addEventListener("click", (event) => {
    event.preventDefault();

    localStorage.removeItem("access_token");
    localStorage.removeItem("user_name");

    window.location.href = "login.html";
  });
});
