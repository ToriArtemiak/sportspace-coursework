
const sportFilter = document.getElementById("sportFilter");
const levelFilter = document.getElementById("levelFilter");
const priceFilter = document.getElementById("priceFilter");

const sessionsList = document.getElementById("sessionsList");
const catalogStatus = document.getElementById("catalogStatus");

// Створення текстового HTML-елемента
function addText(parent, tag, text, className = "") {
    const element = document.createElement(tag);
    element.textContent = text;

    if (className) {
        element.className = className;
    }

    parent.appendChild(element);
    return element;
}

// Створення картки спортивної секції
function createSessionCard(section) {
    const card = document.createElement("article");
    card.className = "session-card";

    addText(card, "span", section.sport_type, "session-type");

    addText(card, "h3", section.name);

    addText(card, "p", `Рівень: ${section.level}`);

    addText(
        card,
        "p",
        `Тренер: ${section.trainer.full_name}`
    );

    addText(
        card,
        "p",
        `Зал: ${section.hall.name}`
    );

    addText(
        card,
        "p",
        `Місто: ${section.hall.center.city}`
    );

    addText(
        card,
        "p",
        `Вік: ${section.min_age}–${section.max_age} років`
    );

    const footer = document.createElement("div");
    footer.className = "session-footer";

    addText(
        footer,
        "strong",
        `${section.price_uah} ₴`
    );

    addText(
        footer,
        "span",
        `Місць у групі: ${section.capacity}`
    );

    card.appendChild(footer);

    return card;
}

// Отримання даних із FastAPI
async function loadSections() {
    catalogStatus.textContent = "Завантаження занять...";
    sessionsList.replaceChildren();

    // Формування параметрів фільтрації
    const params = new URLSearchParams();

    if (sportFilter.value) {
        params.set("sport_type", sportFilter.value);
    }

    if (levelFilter.value) {
        params.set("level", levelFilter.value);
    }

    if (priceFilter.value) {
        params.set("max_price", priceFilter.value);
    }

    try {
        const query = params.toString();
        const url = query
            ? `/api/sections?${query}`
            : "/api/sections";

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const sections = await response.json();

        if (sections.length === 0) {
            catalogStatus.textContent =
                "За вибраними фільтрами занять не знайдено.";
            return;
        }

        // Відображення отриманих секцій
        sections.forEach((section) => {
            const card = createSessionCard(section);
            sessionsList.appendChild(card);
        });

        catalogStatus.textContent =
            `Знайдено занять: ${sections.length}`;

    } catch (error) {
        console.error("Помилка завантаження:", error);

        catalogStatus.textContent =
            "Не вдалося завантажити заняття. Спробуйте оновити сторінку.";
    }
}

// Оновлення каталогу при зміні фільтрів
sportFilter.addEventListener("change", loadSections);
levelFilter.addEventListener("change", loadSections);
priceFilter.addEventListener("change", loadSections);

// Перше завантаження після відкриття сторінки
loadSections();
