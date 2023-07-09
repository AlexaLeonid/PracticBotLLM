from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from nanoid import generate

from kb import make_row_keyboard

router = Router()


import utils.core_utils as core
import utils.conversations_utils as chat

available_llm_names = core.get_models()
llm_names = [item[1] for item in available_llm_names]
available_bot_names = [("skip", "skip")]
prompt_options = [("skip", "skip")]
submit_options = [("submit", "submit")]


class CreatingBot(StatesGroup):
    choosing_llm_name = State()
    choosing_bot_name = State()
    add_system_prompt = State()
    submit_state = State()


@router.callback_query(Text("custom_bot"))
async def create_bot(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text="Создаем системный бот. \n\nВыберите языковую модель:",
        reply_markup=make_row_keyboard(available_llm_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CreatingBot.choosing_llm_name)


@router.callback_query(CreatingBot.choosing_llm_name, Text(llm_names))
async def choose_llm(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    llm_name: str
    for item in available_llm_names:
        if str(item[1]) == callback.data:
            llm_name = item[0]
    await state.update_data(chosen_llm_id=int(callback.data), chosen_llm_name=llm_name)
    await callback.message.answer(
        text="Спасибо. Теперь, пожалуйста, введите имя бота",
        reply_markup=make_row_keyboard(available_bot_names)
    )
    await state.set_state(CreatingBot.choosing_bot_name)


@router.message(CreatingBot.choosing_llm_name)
async def llm_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такой языковой модели.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_llm_names)
    )


@router.message(CreatingBot.choosing_bot_name)
async def add_prompt(message: Message, state: FSMContext):
    await state.update_data(chosen_bot_name=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали имя {user_data['chosen_bot_name']} и языковую модель {user_data['chosen_llm_name']}.\n"
             f"Добавьте промпт",
        reply_markup=make_row_keyboard(prompt_options)
    )
    await state.set_state(CreatingBot.add_system_prompt)


@router.callback_query(CreatingBot.choosing_bot_name, Text("skip"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_bot_name=generate(size=10))
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    await callback.message.answer(
        text=f"Имя вашего проекта {user_data['chosen_bot_name']}, языковая модель {user_data['chosen_llm_name']}.\n"
             f"Добавьте промпт",
        reply_markup=make_row_keyboard(prompt_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingBot.add_system_prompt)


@router.message(CreatingBot.add_system_prompt)
async def submit_bot(message: Message, state: FSMContext):
    await state.update_data(chosen_prompt=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f"Ваш промпт: {user_data['chosen_prompt']}.\n",
        reply_markup=make_row_keyboard(submit_options)
    )
    await state.set_state(CreatingBot.submit_state)


@router.callback_query(CreatingBot.add_system_prompt, Text("skip"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_prompt="")
    user_data = await state.get_data()
    await callback.message.answer(
        "Промпта не будет",
        reply_markup=make_row_keyboard(submit_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingBot.submit_state)


@router.callback_query(CreatingBot.submit_state, Text("submit"))
async def create_bot(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    data = await state.get_data()
    chat.add_bot(callback.message.chat.id, data['chosen_bot_name'], data['chosen_llm_id'],
                data['chosen_prompt'])
    await callback.message.answer(
        text="Бот создан."
    )
    await state.clear()
