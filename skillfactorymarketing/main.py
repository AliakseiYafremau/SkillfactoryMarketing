from os import getenv  # Импортируем функцию для получения переменных окружения
import asyncio  # Импортируем модуль для работы с асинхронным кодом

from aiogram import Bot, Dispatcher, types  # Импортируем необходимые классы из aiogram
from aiogram.filters import CommandStart  # Импортируем фильтр для команды /start

from handlers.user_handlers import user_router  # Импортируем маршрутизатор для обработки пользовательских сообщений
from commands import private  # Импортируем список команд для частных чатов
from db import create_db

from dotenv import load_dotenv  # Импортируем функцию для загрузки переменных окружения из файла

load_dotenv()  # Загружаем переменные окружения из файла .env


bot = Bot(token=getenv("TOKEN"))  # Создаем объект бота, используя токен из переменной окружения

dp = Dispatcher()  # Создаем диспетчер для обработки сообщений и команд

dp.include_router(user_router)  # Подключаем маршрутизатор для обработки пользовательских сообщений


async def main():  # Асинхронная функция для запуска бота
    create_db()
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхук и сбрасываем накопившиеся обновления
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())  # Удаляем все команды в приватных чатах
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())  # Устанавливаем новые команды для приватных чатов
    await dp.start_polling(bot)  # Запускаем polling для обработки сообщений в режиме реального времени


if "__main__" == __name__:  # Проверяем, что файл запущен как основная программа
    asyncio.run(main())  # Запускаем асинхронную функцию main
