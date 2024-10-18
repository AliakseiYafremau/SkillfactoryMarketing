from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton  # Импортируем классы для создания инлайн-клавиатур и кнопок

# Создаем инлайн-клавиатуру с одной кнопкой "add"
intro_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить цель', callback_data='add'),  # Кнопка с текстом "add" и callback_data 'add'
                InlineKeyboardButton(text='Посмотреть цели', callback_data='get'),  # Кнопка с текстом "get" и callback_data 'get'
            ]
        ]
)

# Создаем инлайн-клавиатуру с двумя кнопками: "cancel" и "back"
add_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Отменить', callback_data='cancel'),  # Кнопка "cancel" с callback_data 'cancel'
                InlineKeyboardButton(text='Назад', callback_data='back'),  # Кнопка "back" с callback_data 'back'
            ]
        ]
)

# Создаем инлайн-клавиатуру с одной кнопкой "reset"
reset_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Заново', callback_data='add'),
                InlineKeyboardButton(text='Меню', callback_data='start')  # Кнопка "reset" с callback_data 'add'
            ]
        ]
)

get_goals_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить цель', callback_data='add'),
                InlineKeyboardButton(text='Назад', callback_data='start'),  # Кнопка "back" с callback_data 'back'
            ]
    ]
)
