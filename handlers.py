from aiogram import F, Router, types, Bot
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputFile, CallbackQuery, FSInputFile

import kb
import text

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.main_menu_kb)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.main_menu_kb)


@router.message(Command("menu"))
async def menu(msg: Message):
    await msg.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)


@router.callback_query(Text("settings"))
async def show_settings(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Что поменяем?", reply_markup=kb.settings_kd)


@router.callback_query(Text("extension"))
async def show_extension(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Расширения", reply_markup=kb.extension_kb)


@router.callback_query(Text("upgrade"))
async def show_upgrade(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Выберите план", reply_markup=kb.upgrade_kb)


@router.callback_query(Text("history"))
async def show_history(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("История запросов", reply_markup=kb.make_history_keyboard([]))


@router.callback_query(Text("back"))
async def back_to_manu(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Главное меню для вас", reply_markup=kb.main_menu_kb)


@router.callback_query(Text("projects"))
async def show_projects(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
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
