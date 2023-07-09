from aiogram import F, Router, types, Bot
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputFile, CallbackQuery, FSInputFile


import kb
from utils.core_utils import get_tariffs
import utils.user_utils as user
import text
import utils.user_utils as user
import utils.conversations_utils as chat
import utils.models_utils as model
import utils.core_utils as core
import utils.project_utils as project
router = Router()


available_tariff_type = get_tariffs()
tariff_types = [item[0] for item in available_tariff_type]
available_statistic_type = ["user_statistic", "new_user_statistic"]
available_time_measure = ["day", "month", "year"]
available_time_period = []
submit_options = ["submit"]


class UpdatingPlan(StatesGroup):
    choosing_plan = State()


@router.callback_query(Text("upgrade"))
async def show_upgrade(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Выберите план", reply_markup=kb.make_row_keyboard_1(tariff_types))
    await state.set_state(UpdatingPlan.choosing_plan)


@router.callback_query(UpdatingPlan.choosing_plan, Text(tariff_types))
async def show_upgrade(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    if callback.data == "free":
        user.change_plan(callback.message.chat.id, callback.data)
    else:
        await callback.message.answer(f"Для {callback.data } нужна оплата")
    await state.clear()