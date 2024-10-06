from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from filters import ChatTypeFilter
from keyboards import intro_kb, add_goal_kb, reset_goal_kb

user_router = Router()
user_router.message.filter(ChatTypeFilter(["private"]))

previous_bot_message = None

class AddGoal(StatesGroup):
    name = State()
    amount = State()
    time = State()

    texts = {
        'AddGoal:name': 'Введите название заново:',
        'AddGoal:amount': 'Введите сумму заново:',
        'AddGoal:time': 'Введите срок заново:',
    }

@user_router.message(CommandStart())
async def answer(message: types.Message):
    global previous_bot_message

    m = await message.answer("Привет, Я Бот Финансов. Выберите действие:", reply_markup=intro_kb) 


@user_router.callback_query(StateFilter("*"), F.data == "cancel")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    # await callback_query.message.edit_text("Действие отменено", reply_markup=add_goal_kb)
    await answer(callback_query.message)
    


@user_router.callback_query(StateFilter("*"), F.data == "back")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    current_state = await state.get_state()

    if current_state == AddGoal.name:
        await state.clear()
        # await callback_query.message.edit_text("Действие отменено", reply_markup=add_goal_kb)
        await answer(callback_query.message)
        return
    
    previous_state = await state.get_state()
    for step in AddGoal.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_state)
            await callback_query.message.edit_text(f"Вы вернулись к прошлому шагу \n{AddGoal.texts[previous_state.state]}", reply_markup=add_goal_kb)
        previous_state = step

@user_router.callback_query(F.data == "add")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    await callback_query.message.edit_text("Введите название", reply_markup=add_goal_kb)
    await state.set_state(AddGoal.name)


@user_router.message(AddGoal.name)
async def add_name(message: types.Message, state: FSMContext):
    global previous_bot_message

    await state.update_data(name=message.text)
    await message.answer("Введите сумму, которую вы хотите достичь", reply_markup=add_goal_kb)
    await state.set_state(AddGoal.amount)


@user_router.message(AddGoal.amount)
async def add_amount(message: types.Message, state: FSMContext):
    global previous_bot_message

    await state.update_data(amount=message.text)
    await message.answer("Введите срок,за который вы хотите достичь данной суммы", reply_markup=add_goal_kb)
    await state.set_state(AddGoal.time)


@user_router.message(AddGoal.time)
async def add_time(message: types.Message, state: FSMContext):
    global previous_bot_message
    
    await state.update_data(time=message.text)
    data = await state.get_data()
    await message.answer(f"Вот результат:\n{str(data)}", reply_markup=reset_goal_kb)
    await state.clear()
