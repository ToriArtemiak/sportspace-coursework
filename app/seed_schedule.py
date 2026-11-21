
from datetime import date, time, timedelta

from sqlalchemy import select, func

from app.database import Base, engine, SessionLocal
from app.models import SportsSection, TrainingSession


def seed_schedule():
    Base.metadata.create_all(bind=engine)

    # Назва секції, через скільки днів заняття,
    # час початку та завершення
    schedule = [
        ("Ранкова йога", 1, time(9, 0), time(10, 0)),
        ("Вечірня йога", 2, time(18, 0), time(19, 0)),
        (
            "Функціональний тренінг",
            3,
            time(17, 0),
            time(18, 0)
        ),
        (
            "Плавання для початківців",
            4,
            time(12, 0),
            time(13, 0)
        ),
    ]

    created = 0

    with SessionLocal.begin() as db:
        for name, days_ahead, start, end in schedule:

            section = db.scalar(
                select(SportsSection).where(
                    SportsSection.name == name
                )
            )

            if section is None:
                raise RuntimeError(
                    f"Секцію '{name}' не знайдено. "
                    "Спочатку запусти python -m app.seed"
                )

            training_date = (
                date.today() + timedelta(days=days_ahead)
            )

            # Перевіряємо, чи заняття вже існує
            existing = db.scalar(
                select(TrainingSession).where(
                    TrainingSession.section_id == section.id,
                    TrainingSession.session_date == training_date,
                    TrainingSession.start_time == start
                )
            )

            if existing:
                continue

            new_session = TrainingSession(
                section_id=section.id,
                session_date=training_date,
                start_time=start,
                end_time=end
            )

            db.add(new_session)
            created += 1

    print(f"Створено нових тренувань: {created}")

    with SessionLocal() as db:
        sessions = db.scalars(
            select(TrainingSession).order_by(
                TrainingSession.session_date,
                TrainingSession.start_time
            )
        ).all()

        for session in sessions:
            print(
                f"{session.section.name}: "
                f"{session.session_date} "
                f"{session.start_time.strftime('%H:%M')}"
            )


if __name__ == "__main__":
    seed_schedule()
