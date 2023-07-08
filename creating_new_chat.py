from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from nanoid import generate

from kb import make_row_keyboard

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
# status_options = ["ffff", "uuuu", "kkkkk"]

available_llm_names = [("ChatGPT", "ChatGPT"), ("Claude", "Claude")]
llm_names = ["ChatGPT", "Claude"]
available_chat_names = [("skip", "skip")]
submit_options = [("submit", "submit")]


class CreatingChat(StatesGroup):
    choosing_llm_name = State()
    choosing_chat_name = State()
    submit_state = State()


# @router.message(Command("new_chat"))
@router.callback_query(Text("new_chat"))
async def cmd_food(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text="Создаем новый чат. \n\nВыберите языковую модель:",
        reply_markup=make_row_keyboard(available_llm_names)           #??????????????????
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CreatingChat.choosing_llm_name)


@router.callback_query(CreatingChat.choosing_llm_name, Text(llm_names))
async def food_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await state.update_data(chosen_llm=callback.data)
    await callback.message.answer(
        text="Спасибо. Теперь, пожалуйста, введите имя чата (не обязательно)",
        #  reply_markup=make_row_keyboard(available_food_sizes)
        reply_markup=make_row_keyboard(available_chat_names)
    )
    await state.set_state(CreatingChat.choosing_chat_name)


@router.message(CreatingChat.choosing_llm_name)
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такой языковой модели.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_llm_names)             #??????????????????
    )


@router.message(CreatingChat.choosing_chat_name)
async def food_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_name=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали для чата имя {user_data['chosen_name']} и языковую модель {user_data['chosen_llm']}.\n",
        reply_markup=make_row_keyboard(submit_options)
    )
    await state.set_state(CreatingChat.submit_state)


@router.callback_query(CreatingChat.choosing_chat_name, Text("skip"))
async def food_size_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await state.update_data(chosen_chat_name=generate(size=10))
    user_data = await state.get_data()
    await callback.message.answer(
        text=f"Имя вашего проекта {user_data['chosen_chat_name']}, языковая модель {user_data['chosen_llm']}.\n",
        reply_markup=make_row_keyboard(submit_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingChat.submit_state)


@router.callback_query(CreatingChat.submit_state, Text("submit"))
async def food_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text="Чат создан.",
    )
    await state.clear()
