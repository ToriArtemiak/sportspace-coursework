
const authDialog = document.getElementById("authDialog");
const openAuth = document.getElementById("openAuth");
const closeAuth = document.getElementById("closeAuth");

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const authStatus = document.getElementById("authStatus");

const switchAuth = document.getElementById("switchAuth");
const authTitle = document.getElementById("authTitle");
const authSwitchLabel = document.getElementById("authSwitchLabel");

const accountSection = document.getElementById("accountSection");
const logoutButton = document.getElementById("logoutButton");

let accessToken = null;
let currentUser = null;


// Перемикання між входом і реєстрацією
function setAuthMode(mode) {
    const isLogin = mode === "login";

    loginForm.hidden = !isLogin;
    registerForm.hidden = isLogin;

    authTitle.textContent = isLogin
        ? "Вхід у SportSpace"
        : "Створити акаунт";

    authSwitchLabel.textContent = isLogin
        ? "Ще немає акаунта?"
        : "Вже маєте акаунт?";

    switchAuth.textContent = isLogin
        ? "Зареєструватися"
        : "Увійти";

    authStatus.textContent = "";
}

openAuth.addEventListener("click", () => {
    if (currentUser) {
        accountSection.scrollIntoView({
            behavior: "smooth"
        });
    } else {
        setAuthMode("login");
        authDialog.showModal();
    }
});

closeAuth.addEventListener("click", () => {
    authDialog.close();
});

switchAuth.addEventListener("click", () => {
    setAuthMode(loginForm.hidden ? "login" : "register");
});


// Пояснення помилок API
async function getErrorMessage(response) {
    if (response.status === 409) {
        return "Користувач із таким email вже існує.";
    }

    if (response.status === 401) {
        return "Неправильний email або пароль.";
    }

    if (response.status === 422) {
        return "Перевір правильність введених даних.";
    }

    const data = await response.json().catch(() => null);

    if (typeof data?.detail === "string") {
        return data.detail;
    }

    return "Сталася помилка. Спробуй ще раз.";
}


// Реєстрація
registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const button = registerForm.querySelector(
        "button[type='submit']"
    );

    button.disabled = true;
    authStatus.textContent = "Створюємо акаунт...";

    const userData = {
        full_name: document.getElementById("registerName").value.trim(),
        email: document.getElementById("registerEmail").value.trim(),
        password: document.getElementById("registerPassword").value
    };

    try {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            throw new Error(await getErrorMessage(response));
        }

        registerForm.reset();
        setAuthMode("login");

        document.getElementById("loginEmail").value =
            userData.email;

        authStatus.textContent =
            "Акаунт створено! Тепер увійди.";

    } catch (error) {
        authStatus.textContent = error.message;
    } finally {
        button.disabled = false;
    }
});


// Вхід
loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const button = loginForm.querySelector(
        "button[type='submit']"
    );

    button.disabled = true;
    authStatus.textContent = "Виконуємо вхід...";

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
        const formData = new URLSearchParams({
            username: email.trim(),
            password: password
        });

        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData.toString()
        });

        if (!response.ok) {
            throw new Error(await getErrorMessage(response));
        }

        const tokenData = await response.json();

        // Отримуємо профіль користувача
        const profileResponse = await fetch("/api/auth/me", {
            headers: {
                "Authorization": `Bearer ${tokenData.access_token}`
            }
        });

        if (!profileResponse.ok) {
            throw new Error("Не вдалося отримати профіль.");
        }

        currentUser = await profileResponse.json();
        accessToken = tokenData.access_token;

        showAccount();

        loginForm.reset();
        authDialog.close();

    } catch (error) {
        authStatus.textContent = error.message;
    } finally {
        button.disabled = false;
    }
});


// Відображення профілю
function showAccount() {
    document.getElementById("accountName").textContent =
        currentUser.full_name;

    document.getElementById("accountEmail").textContent =
        currentUser.email;

    document.getElementById("accountRole").textContent =
        currentUser.role === "admin"
            ? "Адміністратор"
            : "Клієнт";

    accountSection.hidden = false;

    openAuth.textContent = "Мій профіль";

    accountSection.scrollIntoView({
        behavior: "smooth"
    });
}


// Вихід з акаунта
logoutButton.addEventListener("click", () => {
    accessToken = null;
    currentUser = null;

    accountSection.hidden = true;
    openAuth.textContent = "Увійти";

    authStatus.textContent = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
});



