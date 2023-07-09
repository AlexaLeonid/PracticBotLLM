from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from nanoid import generate

from kb import make_row_keyboard, main_menu_kb
import utils.conversations_utils as chat
import utils.core_utils as core
import utils.models_utils as model
router = Router()


#available_llm_names = model.get_user_models()
#llm_names = [item[1] for item in available_llm_names]
available_chat_names = [("skip", "skip")]
submit_options = [("submit", "submit")]


class CreatingChat(StatesGroup):
    choosing_llm_name = State()
    choosing_chat_name = State()
    submit_state = State()


@router.callback_query(Text("new_chat"))
async def cmd_food(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    if model.get_count_models(callback.message.chat.id) > 0:
        available_llm_names = model.get_user_models(callback.message.chat.id, 0, 10)
        llm_names = [item[1] for item in available_llm_names]
        print(llm_names)
        await callback.message.answer(
            text="Создаем новый чат. \n\nВыберите языковую модель:",
            reply_markup=make_row_keyboard(available_llm_names)
        )
        # Устанавливаем пользователю состояние "выбирает название"
        await state.set_state(CreatingChat.choosing_llm_name)
        await state.update_data(available_llm_names=available_llm_names, llm_names=llm_names)
    else:
        await callback.message.answer(
            text="Сначала создайте бота:",
            reply_markup=main_menu_kb  # ??????????????????
        )


@router.callback_query(CreatingChat.choosing_llm_name)
async def food_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    data = await state.get_data()
    llm_name: str
    print(callback.data)
    if int(callback.data) in data['llm_names']:
        for item in data['available_llm_names']:
            if str(item[1]) == callback.data:
                llm_name = item[0]
        await state.update_data(chosen_llm_id=callback.data, chosen_llm_name=llm_name)
        await callback.message.answer(
            text="Спасибо. Теперь, пожалуйста, введите имя чата (не обязательно)",
            #  reply_markup=make_row_keyboard(available_food_sizes)
            reply_markup=make_row_keyboard(available_chat_names)
        )
        await state.set_state(CreatingChat.choosing_chat_name)


@router.message(CreatingChat.choosing_llm_name)
async def food_chosen_incorrectly(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        text="Я не знаю такой языковой модели.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(data['available_llm_names'])
    )


@router.message(CreatingChat.choosing_chat_name)
async def food_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_chat_name=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали для чата имя {user_data['chosen_chat_name']} и языковую модель {user_data['chosen_llm_name']}.\n",
        reply_markup=make_row_keyboard(submit_options)
    )
    await state.set_state(CreatingChat.submit_state)


@router.callback_query(CreatingChat.choosing_chat_name, Text("skip"))
async def food_size_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await state.update_data(chosen_chat_name=generate(size=10))
    user_data = await state.get_data()
    await callback.message.answer(
        text=f"Имя вашего проекта {user_data['chosen_chat_name']}, языковая модель {user_data['chosen_llm_name']}.\n",
        reply_markup=make_row_keyboard(submit_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingChat.submit_state)


@router.callback_query(CreatingChat.submit_state, Text("submit"))
async def food_chosen(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    data = await state.get_data()
    chat.add_conversation(callback.message.chat.id, data['chosen_chat_name'], data['chosen_llm_id'])
    await callback.message.answer(
        text="Чат создан.",
    )
    await state.clear()
