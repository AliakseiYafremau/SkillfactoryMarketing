from aiogram.types import BotCommand  # Импортируем класс для создания команд бота

# Определяем список команд для приватных чатов
private = [
    BotCommand(command='start', description='Старт'),  # Команда /start с описанием "Старт"
]
