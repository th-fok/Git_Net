from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os

# Путь к файлу базы данных
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '..', 'planner.db')}"

# Создаем движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Показывать SQL запросы в консоли
    connect_args={"check_same_thread": False}  # Для SQLite
)

def create_db_and_tables():
    """Создает все таблицы в базе данных"""
    SQLModel.metadata.create_all(engine)
    print("✅ База данных и таблицы созданы!")

def get_session() -> Generator[Session, None, None]:
    """Генератор сессий для внедрения зависимостей"""
    with Session(engine) as session:
        yield session

# Функция для инициализации БД при запуске
def init_db():
    create_db_and_tables()