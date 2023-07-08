from aiogram import F, Router, types, Bot
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputFile, CallbackQuery, FSInputFile

import kb
import text

router = Router()

@router.message(Command("menu"))
@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.main_menu_kb)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.main_menu_kb)


"""
@router.message(Command("custom_bot"))
async def menu(msg: Message):
    await msg.answer("Создаем системный бот", reply_markup=kb.custom_bot_kb)


@router.message(Command("new_chat"))
async def menu(msg: Message):
    await msg.answer("Создаем новый чат", reply_markup=kb.new_chat_kb)



@router.message(Command("view_history"))
async def menu(msg: Message):
    await msg.answer("Выберите историю", reply_markup=kb.history_builder.as_markup())
"""


@router.message(Command("menu"))
async def menu(msg: Message):
    await msg.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)


@router.callback_query(Text("settings"))
async def show_settings(callback: CallbackQuery):
    await callback.message.answer("Что поменяем?", reply_markup=kb.settings_kd)

"""
@router.message(Command("change_llm"))
async def menu(msg: Message):
    await msg.answer("На что меняем?", reply_markup=kb.llm_kd)
"""


@router.callback_query(Text("extension"))
async def show_extension(callback: CallbackQuery):
    await callback.message.answer("Расширения", reply_markup=kb.extension_kb)


@router.callback_query(Text("upgrade"))
async def show_upgrade(callback: CallbackQuery):
    await callback.message.answer("Выберите план", reply_markup=kb.upgrade_kb)


@router.callback_query(Text("history"))
async def show_history(callback: CallbackQuery):
    await callback.message.answer("История запросов", reply_markup=kb.make_history_keyboard([]))


@router.callback_query(Text("back"))
async def back_to_manu(callback: CallbackQuery):
    await callback.message.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)


@router.callback_query(Text("projects"))
async def show_projects(callback: CallbackQuery):
    await callback.message.answer("Ваши проекты")


@router.callback_query(Text("cancel"))
async def state_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Отмена")
    await callback.message.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)
    await state.clear()


@router.message(Command("file"))
async def send_file(msg: Message, bot: Bot):
    file = FSInputFile('C:\\Users\\Sasacompik\\OneDrive\\Рабочий стол\\test.txt')
    await bot.send_document(chat_id=msg.chat.id, document=file)




"""
@router.message(F.document)
async def handle_docs_photo(msg: Message, bot: Bot):
    chat_id = msg.chat.id

    file_info = await bot.get_file(msg.document.file_id)
    file_ext = msg.document.file_name.split(".")[1]
    src = 'C:\\Users\\Sasacompik\\OneDrive\\Рабочий стол\\College\\Практика\\files\\' + msg.document.file_name
    await bot.download_file(file_info.file_path, src)

    if file_ext == "txt" or file_ext == "doc":
        f = open(src, 'r', encoding='UTF-8')
        jokes = f.read()
        await msg.answer(jokes)
"""

# await msg.answer("Пожалуй, я сохраню это")
#  await msg.answer(file_ext)
