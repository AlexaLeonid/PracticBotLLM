from aiogram import Router, F, Bot
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from nanoid import generate
from kb import make_row_keyboard
import utils.project_utils as project
import utils.core_utils as core

router = Router()


available_llm_names = core.get_models()
#available_llm_names = [("fgfgfg", "1")]
llm_names = [item[1] for item in available_llm_names]
available_project_names = [("skip", "skip")]
prompt_options = [("skip", "skip")]
file_options = []
submit_options = [("submit", "submit")]


class CreatingProject(StatesGroup):
    choosing_llm_name = State()
    choosing_project_name = State()
    add_system_prompt = State()
    add_file = State()
    submit_state = State()


@router.callback_query(Text("add_project"))
async def add_project(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    if project.checking_project_access(callback.from_user.id):
        await callback.message.answer(
        text="Создаем проект. \n\nВыберите языковую модель:",
        reply_markup=make_row_keyboard(available_llm_names)
        )
        # Устанавливаем пользователю состояние "выбирает название"
        await state.set_state(CreatingProject.choosing_llm_name)
    else:
        await callback.message.answer(
            text="Ваш тариф не предусматривает такой опции"
        )


@router.callback_query(CreatingProject.choosing_llm_name, Text(llm_names))
async def choose_name(callback: CallbackQuery, state: FSMContext):
    llm_name: str
    for item in available_llm_names:
        if str(item[1]) == callback.data:
            llm_name = item[0]
    await state.update_data(chosen_llm_id=int(callback.data), chosen_llm_name=llm_name)
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text="Спасибо. Теперь, пожалуйста, введите имя проекта",
        reply_markup=make_row_keyboard(available_project_names)
    )
    await state.set_state(CreatingProject.choosing_project_name)


@router.message(CreatingProject.choosing_llm_name)
async def wrong_llm(message: Message):
    await message.edit_reply_markup()
    await message.answer(
        text="Я не знаю такой языковой модели.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_llm_names)
    )


@router.message(CreatingProject.choosing_project_name)
async def add_prompt(message: Message, state: FSMContext):
    await state.update_data(chosen_project_name=message.text)
    await message.edit_reply_markup()
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали имя {user_data['chosen_project_name']} и языковую модель {user_data['chosen_llm_name']}.\n"
             f"Добавьте промпт",
        reply_markup=make_row_keyboard(prompt_options)
    )
    await state.set_state(CreatingProject.add_system_prompt)


@router.callback_query(CreatingProject.choosing_project_name, Text("skip"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_project_name=generate(size=10))
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    await callback.message.answer(
        text=f"Имя вашего проекта {user_data['chosen_project_name']}, языковая модель {user_data['chosen_llm_name']}.\n"
             f"Добавьте промпт",
        reply_markup=make_row_keyboard(prompt_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingProject.add_system_prompt)


@router.message(CreatingProject.add_system_prompt)
async def add_file(message: Message, state: FSMContext):
    await state.update_data(chosen_prompt=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f"Ваш промпт: {user_data['chosen_prompt']}.\n"
             f"Добавьте файл",
        reply_markup=make_row_keyboard(file_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingProject.add_file)


@router.callback_query(CreatingProject.add_system_prompt, Text("skip"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_prompt="")
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    await callback.message.answer(
        "Добавьте файл",
        reply_markup=make_row_keyboard(file_options)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.set_state(CreatingProject.add_file)


@router.message(CreatingProject.add_file, F.document)
async def submit_project(msg: Message, bot: Bot, state: FSMContext):
    file_info = await bot.get_file(msg.document.file_id)
    MyBinaryIO = await bot.download_file(file_info.file_path)
    await state.update_data(chosen_file=MyBinaryIO, mimetype=msg.document.mime_type)
    file_ext = msg.document.file_name.split(".")[1]
    src = 'C:\\Users\\Sasacompik\\OneDrive\\Рабочий стол\\College\\Практика\\files\\' + msg.document.file_name
   # await bot.download_file(file_info.file_path, src)
    await msg.answer(
        text="Файл добавлен. Подтверждаем проект?",
        reply_markup=make_row_keyboard(submit_options)
    )
    await state.set_state(CreatingProject.submit_state)
"""
    if file_ext == "txt" or file_ext == "doc":
        f = open(src, 'r', encoding='UTF-8')
        jokes = f.read()
        await msg.answer(jokes)
"""


@router.callback_query(CreatingProject.submit_state, Text("submit"))
async def create_project(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    data = await state.get_data()
    project.add_user_project(callback.message.chat.id, data['chosen_project_name'], data['mimetype'], data['chosen_llm_id'],
                             data['chosen_prompt'], data['chosen_file'])
    await callback.message.answer(
        text="Проект создан."
    )
    await state.clear()




