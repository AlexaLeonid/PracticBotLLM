from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from kb import make_row_keyboard, main_menu_kb
from utils import generate_random_string

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_llm_names = ["ChatGPT", "ulululu", "qwqwq"]
available_bot_names = ["skip"]
prompt_options = []
submit_options = ["submit"]


class CreatingBot(StatesGroup):
    choosing_llm_name = State()
    choosing_bot_name = State()
    add_system_prompt = State()
    submit_state = State()


# @router.message(Command("custom_bot"))
@router.callback_query(Text("custom_bot"))
async def create_bot(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text="Создаем системный бот. \n\nВыберите языковую модель:",
        reply_markup=make_row_keyboard(available_llm_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CreatingBot.choosing_llm_name)


@router.callback_query(CreatingBot.choosing_llm_name, Text(available_llm_names))
async def choose_llm(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await state.update_data(chosen_llm=callback.data)
    await callback.message.answer(
        text="Спасибо. Теперь, пожалуйста, введите имя бота",
        reply_markup=make_row_keyboard(available_bot_names)
    )
    await state.set_state(CreatingBot.choosing_bot_name)


@router.message(CreatingBot.choosing_llm_name)
async def llm_chosen_incorrectly(message: Message):
    await message.edit_reply_markup()
    await message.answer(
        text="Я не знаю такой языковой модели.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_llm_names)
    )


@router.message(CreatingBot.choosing_bot_name)
async def add_prompt(message: Message, state: FSMContext):
    await state.update_data(chosen_bot_name=message.text)
    await message.edit_reply_markup()
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали имя {user_data['chosen_bot_name']} и языковую модель {user_data['chosen_llm']}.\n"
             f"Добавьте промпт",
        reply_markup=make_row_keyboard(prompt_options)
    )
    await state.set_state(CreatingBot.add_system_prompt)


@router.callback_query(CreatingBot.choosing_bot_name, Text("skip"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_bot_name=generate_random_string(8))
    user_data = await state.get_data()
    await callback.message.answer(
        text=f"Имя вашего проекта {user_data['chosen_bot_name']}, языковая модель {user_data['chosen_llm']}.\n"
             f"Добавьте промпт",
        reply_markup=make_row_keyboard(prompt_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingBot.add_system_prompt)


@router.message(CreatingBot.add_system_prompt)
async def submit_bot(message: Message, state: FSMContext):
    await state.update_data(chosen_prompt=message.text)
    await message.edit_reply_markup()
    user_data = await state.get_data()
    await message.answer(
        text=f"Ваш промпт: {user_data['chosen_prompt']}.\n",
        reply_markup=make_row_keyboard(submit_options)
    )
    await state.set_state(CreatingBot.submit_state)


@router.callback_query(CreatingBot.submit_state, Text("submit"))
async def create_bot(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text="Бот создан."
    )
    await state.clear()
