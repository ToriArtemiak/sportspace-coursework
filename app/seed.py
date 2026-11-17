
from sqlalchemy import select, func

from app.database import Base, engine, SessionLocal
from app.models import (
    SportsCenter,
    SportsHall,
    Trainer,
    SportsSection,
)


def get_or_create(session, model, lookup, **values):
    """Знаходить запис або створює новий."""

    instance = session.scalar(
        select(model).filter_by(**lookup)
    )

    if instance is None:
        instance = model(**lookup, **values)
        session.add(instance)
        session.flush()

    return instance


def seed_database():
    # Створюємо таблиці, якщо вони відсутні
    Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as session:

        # 1. Спортивний центр
        center = get_or_create(
            session,
            SportsCenter,
            {"name": "SportSpace Lviv"},
            city="Львів",
            address="Демонстраційна адреса, 1",
        )

        # 2. Спортивні зали
        halls_data = [
            ("Зал йоги", 18),
            ("Фітнес-зал", 30),
            ("Басейн", 20),
        ]

        halls = {}

        for name, capacity in halls_data:
            halls[name] = get_or_create(
                session,
                SportsHall,
                {
                    "name": name,
                    "sport_center_id": center.id,
                },
                capacity=capacity,
            )

        # 3. Тренери
        trainers_data = [
            ("Олена Коваль", "Йога", 6),
            ("Андрій Мельник", "Фітнес", 8),
            ("Марія Бондар", "Плавання", 5),
        ]

        trainers = {}

        for name, specialization, experience in trainers_data:
            trainers[name] = get_or_create(
                session,
                Trainer,
                {"full_name": name},
                specialization=specialization,
                experience_years=experience,
            )

        # 4. Спортивні секції
        sections_data = [
            (
                "Ранкова йога", "Йога", "Початковий",
                16, 65, 15, 250,
                "Зал йоги", "Олена Коваль"
            ),
            (
                "Вечірня йога", "Йога", "Середній",
                16, 65, 15, 300,
                "Зал йоги", "Олена Коваль"
            ),
            (
                "Функціональний тренінг", "Фітнес",
                "Усі рівні",
                16, 60, 22, 350,
                "Фітнес-зал", "Андрій Мельник"
            ),
            (
                "Плавання для початківців", "Плавання",
                "Початковий",
                8, 60, 12, 400,
                "Басейн", "Марія Бондар"
            ),
        ]

        for (
            name, sport_type, level,
            min_age, max_age, capacity, price,
            hall_name, trainer_name
        ) in sections_data:

            get_or_create(
                session,
                SportsSection,
                {
                    "name": name,
                    "hall_id": halls[hall_name].id,
                    "trainer_id": trainers[trainer_name].id,
                },
                sport_type=sport_type,
                level=level,
                min_age=min_age,
                max_age=max_age,
                capacity=capacity,
                price_uah=price,
            )

    print("Демонстраційні дані успішно підготовлено!")

    # Виводимо кількість записів
    with SessionLocal() as session:
        tables = [
            ("Центри", SportsCenter),
            ("Зали", SportsHall),
            ("Тренери", Trainer),
            ("Секції", SportsSection),
        ]

        for title, model in tables:
            count = session.scalar(
                select(func.count()).select_from(model)
            )
            print(f"{title}: {count}")


if __name__ == "__main__":
    seed_database()
