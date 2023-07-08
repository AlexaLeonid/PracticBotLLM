from aiogram import Router, Bot
from aiogram.filters import Command, Text, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile

import matplotlib.pyplot as plt
import numpy as np
import numexpr

import admin_kb
import kb

router = Router()

available_tariff_type = ["free", "basic", "advanced"]

available_statistic_type = ["user_statistic", "new_user_statistic"]
available_time_measure = ["day", "month", "year"]
available_time_period = []
submit_options = ["submit"]

#class SettingTariff(StatesGroup)


class CreatingStatistic(StatesGroup):
    choosing_statistic_type = State()
    choosing_time_measure = State()
    choosing_time_period = State()
    submit_state = State()


@router.message(Command("admin"))
async def menu(msg: Message):
    # if msg.from_user.id ==
    await msg.answer("Приветсвуем, о мудрейший", reply_markup=admin_kb.start_kd)


@router.callback_query(Text("view_statistics"))
async def choose_statistic(callback: CallbackQuery, state: FSMContext):
    # if msg.from_user.id ==
    await callback.message.edit_reply_markup()
    await callback.message.answer("Какая статистика интересует?", reply_markup=kb.make_row_keyboard(available_statistic_type))
    await state.set_state(CreatingStatistic.choosing_statistic_type)


# await msg.answer("Вы не админ")


@router.callback_query(CreatingStatistic.choosing_statistic_type, Text(available_statistic_type))
async def choose_period_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_statistic_type=callback.data)
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    await callback.message.answer(
        text=f"Вы выбрали статистику {user_data['chosen_statistic_type']}, мудрейший. \nТеперь, пожалуйста, выберите вид периода",
        reply_markup=kb.make_row_keyboard(available_time_measure)
    )
    await state.set_state(CreatingStatistic.choosing_time_measure)


@router.callback_query(CreatingStatistic.choosing_time_measure, Text(available_time_measure))
async def choose_period_length(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chosen_time_mesure=callback.data)
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    await callback.message.answer(
        text="Теперь, пожалуйста, введите длительность периода (число)"
    )
    await state.set_state(CreatingStatistic.choosing_time_period)


@router.message(CreatingStatistic.choosing_time_period)
async def submit_statistic(message: Message, state: FSMContext):
    await state.update_data(chosen_time_period=message.text)
    await message.edit_reply_markup()
    user_data = await state.get_data()
    await message.answer(
        text=F"Вы выбрали {user_data['chosen_statistic_type']} за {user_data['chosen_time_period']} {user_data['chosen_time_mesure']}(s)",
        reply_markup=kb.make_row_keyboard(submit_options)
    )
    await state.set_state(CreatingStatistic.submit_state)


@router.callback_query(CreatingStatistic.submit_state, Text("submit"))
async def create_statistic(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        text="Статистика создана."
    )
    await state.clear()


@router.message(Command("grant"))
async def grant_tariff(message: Message, command: CommandObject):
    text = command.args
    args = text.split(" ")
    if args[0] in available_tariff_type:
        await message.answer(text)
    else:
        types = ""
        for tariff in available_tariff_type:
            types += "\n* " + tariff
        await message.answer("Такого тарифа нет.\n Доступные: " + types)


@router.message(Command("graph"))
async def send_graph(message: Message, bot: Bot):
    x = np.linspace(-10, 10, 10)
    """
    y = numexpr.evaluate('x**2')  # message.text = 'x**2'
    plt.plot(x, y, 'r')
    plt.savefig('plot_name.png', dpi=300)
    """

    plt.plot([1, 2, 3, 4], [1, 5, 3, 10])
    plt.xticks([1, 2, 3, 4])
    plt.yticks([1, 5, 3, 10])
    plt.xlabel('день', fontsize=16)
    plt.ylabel('Прирост новых пользователей', fontsize=16)
    plt.title('Статистика новых пользователй')

    # включаем основную сетку
    plt.grid(which='major')
    # включаем дополнительную сетку
  #  plt.grid(which='minor', linestyle=':')
    plt.tight_layout()
    plt.savefig('plot_name.png', dpi=300)
    graph = FSInputFile('plot_name.png')
    await bot.send_photo(message.chat.id, photo=graph)
    await message.answer("Ваша статистика, мудрейший")
"""
  fig = plt.figure()
    fig.patch.set_alpha(0.3)
    fig.patch.set_facecolor('blue')

    ax = fig.add_subplot(111)
 #   ax.patch.set_facecolor('orange')
    ax.patch.set_alpha(0.0)
"""
