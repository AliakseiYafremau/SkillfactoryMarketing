from aiogram.filters import Filter  # Импортируем базовый класс фильтра
from aiogram import types  # Импортируем необходимые типы из aiogram

# Определяем фильтр для проверки типа чата
class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:  # Конструктор принимает список типов чатов
        self.chat_types = chat_types  # Сохраняем список типов чатов

    # Метод, который вызывается при проверке фильтра
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types  # Возвращаем True, если тип чата сообщения совпадает с допустимыми типами
