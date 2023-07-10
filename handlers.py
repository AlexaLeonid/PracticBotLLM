from aiogram import F, Router, types, Bot
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputFile, CallbackQuery, FSInputFile


import kb
import text
import utils.user_utils as user
import utils.conversations_utils as chat
import utils.models_utils as model
import utils.core_utils as core
import utils.project_utils as project
router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    user.login(msg.from_user.id, msg.from_user.username)
 #   data = user.get_user(msg.from_user.id)
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.main_menu_kb)


@router.message(Command("menu"))
async def main_menu(msg: Message):
    await msg.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)


@router.callback_query(Text("settings"))
async def show_settings(callback: CallbackQuery):
    sub, tokens, llm = user.get_user(callback.message.chat.id)
    data = "Subscription: " + sub + "\nТокены: " + str(tokens) + "\nМодель по умолчанию: " + llm
    await callback.message.edit_reply_markup()
    await callback.message.answer(data, reply_markup=kb.settings_kd)


@router.callback_query(Text("extension"))
async def show_extension(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Расширения", reply_markup=kb.extension_kb)

"""
@router.callback_query(Text("upgrade"))
async def show_upgrade(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Выберите план", reply_markup=kb.upgrade_kb)
"""


@router.callback_query(Text("back"))
async def back_to_manu(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)


@router.callback_query(Text("cancel"))
async def state_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Отмена")
    await callback.message.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)
    await state.clear()

"""
@router.message(Command("file"))
async def send_file(msg: Message, bot: Bot):
    file = FSInputFile('C:\\Users\\Sasacompik\\OneDrive\\Рабочий стол\\test.txt')
    await bot.send_document(chat_id=msg.chat.id, document=file)
"""


@router.message(F.text)
async def ask(msg: Message, bot: Bot):
    if model.get_count_models(msg.chat.id) > 0:
        if chat.get_count_conversations(msg.chat.id) > 0:
            await msg.answer("Запрос обрабатывается...")
            await msg.answer(core.ask(msg.chat.id, msg.text))
        else:
            await msg.answer("Нужно создать чат", reply_markup=kb.main_menu_kb)
    else:
        await msg.answer("Нужно создать системный бот, потом чат", reply_markup=kb.main_menu_kb)