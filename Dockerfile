# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем pyproject.toml и poetry.lock в контейнер
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Копируем код бота в контейнер
COPY ./skillfactorymarketing ./skillfactorymarketing

# Указываем команду для запуска бота
CMD ["poetry", "run", "python", "skillfactorymarketing/main.py"]
