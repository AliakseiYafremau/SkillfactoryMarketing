# Импортируем необходимые библиотеки из пакета aiogram
from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

# Импортируем ceil() из библиотеки math для укругления результата
from math import ceil

from filters import ChatTypeFilter  # Импортируем фильтры
from keyboards import intro_kb, add_goal_kb, reset_goal_kb, get_goals_kb  # Импортируем клавиатуры
from db import add_db_goal, get_db_goals, delete_db_goal  # Импортируем функции для работы с базой данных

user_router = Router()  # Создаем роутер для приватных сообщений
user_router.message.filter(ChatTypeFilter(["private"]))  # Применяем фильтр для обработки только приватных сообщений

# Класс состояний для добавления цели
class AddGoal(StatesGroup):
    name = State()  # Состояние для ввода названия цели
    amount = State()  # Состояние для ввода суммы цели
    time = State()  # Состояние для ввода срока

    last_message = State()  # Состояние для хранения ID последнего сообщения бота

    # Словарь с текстами при отступлении на шаг назад
    texts = {
        'AddGoal:name': 'Введите название заново:',
        'AddGoal:amount': 'Введите сумму заново:',
        'AddGoal:time': 'Введите срок заново:',
    }

# Хэндлер для команды /start
@user_router.message(CommandStart())
async def start_answer(message: types.Message):
    await message.answer("Привет, <i>Я Бот Финансов</i>."
                         "С помощью меня вы можете высчитать сумму, которую вам необходимо откладывать для достижения цели.\n"
                         "Выберите действие:", reply_markup=intro_kb, parse_mode=ParseMode.HTML)  # Отправляем приветственное сообщение с клавиатурой
    return


# Хэндлер для обработки нажатия кнопки "start"
@user_router.callback_query(F.data == "start")
async def start(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Привет, <i>Я Бот Финансов</i>."
                         "С помощью меня вы можете высчитать сумму, которую вам необходимо откладывать для достижения цели.\n"
                         "Выберите действие:", reply_markup=intro_kb, parse_mode=ParseMode.HTML)  # Отправляем приветственное сообщение с клавиатурой
    return


# Хэндлер для обработки нажатия кнопки "cancel"
@user_router.callback_query(StateFilter("*"), F.data == "cancel")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()  # Получаем текущее состояние FSM
    if current_state is None:
        return  # Если состояния нет, просто выходим
    await state.clear()  # Очищаем состояние
    await start_answer(callback_query.message)  # Возвращаемся к стартовому сообщению


# Хэндлер для обработки нажатия кнопки "back"
@user_router.callback_query(StateFilter("*"), F.data == "back")
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()  # Получаем текущее состояние FSM

    if current_state == AddGoal.name:
        await state.clear()  # Если текущее состояние — AddGoal.name, очищаем состояние и возвращаемся к началу
        await start_answer(callback_query.message)

    previous_state = await state.get_state()  # Получаем предыдущее состояние
    for step in AddGoal.__all_states__:  # Проходим по всем состояниям
        if step.state == current_state:
            await state.set_state(previous_state)  # Устанавливаем предыдущее состояние
            await callback_query.message.edit_text(
                f"Вы вернулись к прошлому шагу \n{AddGoal.texts[previous_state.state]}", reply_markup=add_goal_kb
            )  # Обновляем сообщение, указывая на возврат к предыдущему шагу
        previous_state = step  # Обновляем предыдущее состояние

@user_router.callback_query(F.data == "get")
async def view_goals(callback_query: types.CallbackQuery):
    goals = get_db_goals(callback_query.from_user.id)  # Получаем цели из базы данных
    if not goals:
        await callback_query.message.edit_text("У вас пока нет сохраненных целей.", reply_markup=get_goals_kb)
        return

    goals_text = ""
    goal_list = []

    for goal in goals:
        # Добавляем информацию о цели в текст
        goals_text += (
            f"Цель: <b>{goal.name}</b>\n"
            f"Сумма: {goal.amount}₽\n"
            f"Срок: {goal.time} месяцев\n"
            f"Ежемесячные накопления: {goal.monthly_savings}₽\n\n"
        )

        # Добавляем инлайн-кнопку для удаления каждой цели
        goal_list.append([
            types.InlineKeyboardButton(
                text=f"Удалить {goal.name}",
                callback_data=f"delete_goal:{goal.id}"  # Генерируем callback_data с идентификатором цели
            )]
        )
    goal_kb = types.InlineKeyboardMarkup(inline_keyboard=goal_list)
    
    await callback_query.message.edit_text(goals_text, reply_markup=goal_kb, parse_mode=ParseMode.HTML)
    return



# Хэндлер для нажатия кнопки "add" для начала ввода цели
@user_router.callback_query(F.data == "add")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    sent_message = await callback_query.message.edit_text("Введите название вашей цели", reply_markup=add_goal_kb)  # Редактируем сообщение для ввода названия цели
    await state.set_state(AddGoal.name)  # Устанавливаем состояние для ввода названия
    await state.update_data(last_message_id=sent_message.message_id)  # Сохраняем ID последнего сообщения в FSM

# Хэндлер для ввода названия цели
@user_router.message(AddGoal.name)
async def add_name(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)  # Сохраняем название цели в FSM
    await message.delete()  # Удаляем сообщение пользователя с названием
    data = await state.get_data()  # Получаем данные из FSM
    
    last_message_id = data.get('last_message_id')  # Получаем ID последнего сообщения

    # Обновляем последнее сообщение с введенным названием
    await bot.edit_message_text(
        f"Название: <b>{data['name']}</b>\nВведите сумму(₽), которую вы хотите достичь",
        chat_id=message.chat.id,
        message_id=last_message_id,
        reply_markup=add_goal_kb,
        parse_mode=ParseMode.HTML
    )
    await state.set_state(AddGoal.amount)  # Устанавливаем состояние для ввода суммы

# Хэндлер для ввода суммы цели
@user_router.message(AddGoal.amount)
async def add_amount(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(amount=message.text)  # Сохраняем сумму цели в FSM
    await message.delete()  # Удаляем сообщение пользователя с суммой
    data = await state.get_data()  # Получаем данные из FSM

    last_message_id = data.get('last_message_id')  # Получаем ID последнего сообщения

    # Обновляем последнее сообщение с введенной суммой
    await bot.edit_message_text(
        f"Название: <b>{data['name']}</b>\nСумма: <b>{data['amount']}₽</b>\nВведите количество месяцев, за которое вы хотите достичь данной суммы",
        chat_id=message.chat.id,
        message_id=last_message_id,
        reply_markup=add_goal_kb,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(AddGoal.time)  # Устанавливаем состояние для ввода срока

# Хэндлер для ввода срока цели
@user_router.message(AddGoal.time)
async def add_time(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(time=message.text)  # Сохраняем срок цели в FSM
    data = await state.get_data()  # Получаем данные из FSM
    await message.delete()  # Удаляем сообщение пользователя со сроком

    last_message_id = data.get('last_message_id')  # Получаем ID последнего сообщения
    result = ceil(float(data['amount']) / float(data['time'])) # Высчитываем результат

    try:
        add_db_goal(
            user_id=message.from_user.id,
            name=data['name'],
            amount=float(data['amount']),
            time=int(data['time']),
            monthly_savings=result
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении цели: {str(e)}")
        return

    # Обновляем последнее сообщение с итоговой информацией о цели
    if data['time'] != 1:
        await bot.edit_message_text(
            f"Название: {data['name']}\n"
            f"Сумма: {data['amount']}₽\n"
            f"Срок: {data['time']} месяц\n\n"
            f"Вы сможете накопить на вашу цель({data['name']}) в течении {data['time']}, если будете откладывать в месяц по {result}₽ в месяц",
            chat_id=message.chat.id,
            message_id=last_message_id,
            reply_markup=reset_goal_kb,
            parse_mode=ParseMode.HTML
        )
    else:
        await bot.edit_message_text(
            f"Название: {data['name']}\n"
            f"Сумма: {data['amount']}₽\n"
            f"Срок: {data['time']} месяцев\n\n"
            f"Вы сможете накопить на вашу цель({data['name']}) в течении {data['time']}, если будете откладывать в месяц по {result}₽ в месяц",
            chat_id=message.chat.id,
            message_id=last_message_id,
            reply_markup=reset_goal_kb,
            parse_mode=ParseMode.HTML
        )
    await state.clear()  # Очищаем состояние после завершения процесса

@user_router.callback_query(F.data.startswith("delete_goal:"))
async def delete_goal_callback(callback_query: types.CallbackQuery):
    goal_id = int(callback_query.data.split(":")[1])  # Получаем ID цели из callback_data

    # Удаляем цель из базы данных
    delete_db_goal(goal_id)

    # Обновляем сообщение, удаляя кнопку
    await callback_query.message.edit_text("Цель удалена.", reply_markup=get_goals_kb)