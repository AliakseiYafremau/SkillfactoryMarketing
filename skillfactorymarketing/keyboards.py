from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


intro_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='add', callback_data='add'),
            ]
        ]
)

add_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='cancel', callback_data='cancel'),
                InlineKeyboardButton(text='back', callback_data='back'),
            ]
        ]
)

reset_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='reset', callback_data='add'),
            ]
        ]
)