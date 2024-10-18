# db.py
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()

# Настраиваем подключение к базе данных SQLite
DATABASE_URL = "sqlite:///goals.db"
engine = create_engine(DATABASE_URL)

# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определяем модель цели
class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    time = Column(Integer, nullable=False)
    monthly_savings = Column(Float, nullable=False)

# Создаем таблицы в базе данных
def create_db():
    Base.metadata.create_all(bind=engine)

# Функция для добавления новой цели в базу данных
def add_db_goal(user_id: int, name: str, amount: float, time: int, monthly_savings: float):
    session = SessionLocal()  # Создаем сессию
    try:
        new_goal = Goal(
            user_id=user_id,
            name=name,
            amount=amount,
            time=time,
            monthly_savings=monthly_savings
        )
        session.add(new_goal)  # Добавляем цель
        session.commit()  # Фиксируем изменения
    except Exception as e:
        session.rollback()  # Откатываем изменения при ошибке
        raise e
    finally:
        session.close()  # Закрываем сессию

# Функция для получения всех целей пользователя
def get_db_goals(user_id: int):
    session = SessionLocal()  # Создаем сессию
    try:
        return session.query(Goal).filter_by(user_id=user_id).all()  # Получаем все цели пользователя
    except Exception as e:
        raise e
    finally:
        session.close()  # Закрываем сессию

def delete_db_goal(goal_id: int):
    engine = create_engine('sqlite:///goals.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    goal = session.query(Goal).filter(Goal.id == goal_id).first()
    if goal:
        session.delete(goal)
        session.commit()
    session.close()