from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, BufferedInputFile

from kb import make_row_keyboard, make_history_keyboard, make_row_keyboard_1, make_history_keyboard_1
import text
import utils.user_utils as user
import utils.conversations_utils as chat

router = Router()


class ShowingChats(StatesGroup):
    show_chats = State()
    show_convo = State()


@router.callback_query(Text("history"))
async def show_projects(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    p_count = chat.get_count_conversations(callback.message.chat.id)
    print(p_count)
    c = 0
    chats = []
    if c < p_count:
        chats = chat.get_conversations(callback.message.chat.id, c, 10)
        c += 10
        await callback.message.answer("История чатов", reply_markup=make_history_keyboard(chats))
        await state.set_state(ShowingChats.show_chats)
        await state.update_data(c=c, ch_count=p_count)
    else:
        await callback.message.answer("История чатов", reply_markup=make_history_keyboard(chats))


@router.callback_query(ShowingChats.show_chats, Text("next"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    c = user_data['c']
    p_count = user_data['ch_count']
    projects = [str]
    if c < p_count:
        projects = chat.get_conversations(callback.message.chat.id, c, 10)
        c += 10
        projects.append("next")
        await callback.message.answer("", reply_markup=make_history_keyboard_1(projects))
        await state.update_data(c=c)
    else:
        projects = chat.get_conversations(callback.message.chat.id, c, 10)
        await callback.message.answer("Конец списка чатов", reply_markup=make_history_keyboard_1(projects))


@router.callback_query(ShowingChats.show_chats)
async def show_projects(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await state.update_data(chat_id=callback.data)
    msg_count = chat.get_count_msg(callback.message.chat.id, callback.data)
    print(msg_count)
    c = 0
    if c < msg_count:
        mgs = chat.get_conversation(callback.data, c, 10)
        print(mgs)
        c += 10
        convo = ""
        for item in mgs:
            convo += "Вы: " + item[0] + "\n\n" + "Бот: " + item[1] + "\n\n"
        print(convo)
        await callback.message.answer("История чата\n\n" + convo, reply_markup=make_history_keyboard([]))
        await state.set_state(ShowingChats.show_convo, )
        await state.update_data(c=c, msg_count=msg_count)
    else:
        await callback.message.answer("Конец истории чата\n\n", reply_markup=make_row_keyboard([]))


@router.callback_query(ShowingChats.show_convo, Text("next"))
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    user_data = await state.get_data()
    c = user_data['c']
    msg_count = user_data['msg_count']
    mgs = [str]
    if c < msg_count:
        mgs = chat.get_conversation(callback.data, c, 10)
        c += 10
        convo: str
        for item in mgs:
            convo.join("Вы: " + item[0] + "\n").join("Бот: " + item[1] + "\n")
        await callback.message.answer(convo, reply_markup=make_history_keyboard([]))
        await state.set_state(ShowingChats.show_convo, )
        await state.update_data(c=c, msg_count=msg_count)
    else:
        await callback.message.answer("Конец истории чата\n\n", reply_markup=make_row_keyboard([]))
