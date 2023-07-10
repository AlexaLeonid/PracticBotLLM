from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, BufferedInputFile

from kb import make_row_keyboard, make_history_keyboard, menu_kb, main_menu_kb
import text
import utils.user_utils as user
import utils.project_utils as project

router = Router()


class ShowingProject(StatesGroup):
    show_projects = State()


@router.callback_query(Text("projects"))
async def show_projects(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    p_count = project.get_count_projects(callback.message.chat.id)
    print(p_count)
    c = 0
    projects = []
    if c < p_count:
        projects = project.get_user_projects(callback.message.chat.id, c, 10)
        c += 10
       # projects.append("next")

        await callback.message.answer("Ваши проекты", reply_markup=make_history_keyboard(projects))
        await state.set_state(ShowingProject.show_projects)
        await state.update_data(c=c, p_count=p_count)
    else:
        await callback.message.answer("Ваши проекты", reply_markup=make_row_keyboard(projects))


@router.callback_query(ShowingProject.show_projects, Text("next"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    c = user_data['c']
    p_count = user_data['p_count']
    projects = [str]
    if c < p_count:
        projects = project.get_user_projects(callback.message.chat.id, c, 10)
        c += 10
        await callback.message.answer("", reply_markup=make_history_keyboard(projects))
        await state.update_data(c=c)
    else:
        projects = project.get_user_projects(callback.message.chat.id, c-10, 10)
        await callback.message.answer("Конец списка проектов", reply_markup=make_row_keyboard(projects))


@router.callback_query(ShowingProject.show_projects, Text("back"))
async def skip_name(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_reply_markup()
    await state.clear()
    await callback.message.answer("Главное меню", reply_markup=main_menu_kb)

"""
@router.callback_query(ShowingProject.show_projects)
async def skip_name(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_reply_markup()
    await state.clear()
    await callback.message.answer("Главное меню", reply_markup=main_menu_kb)
"""


@router.callback_query(ShowingProject.show_projects)
async def skip_name(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_reply_markup()
    data, file_name = project.get_user_project(callback.data)
    await callback.message.answer("Ваш проект:\n", reply_markup=menu_kb)
    await bot.send_document(chat_id=callback.message.chat.id, document=BufferedInputFile(data, file_name))
    await state.clear()
