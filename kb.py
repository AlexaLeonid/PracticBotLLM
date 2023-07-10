from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove


start_menu = [[KeyboardButton(text="/menu")]]
menu_kb = ReplyKeyboardMarkup(keyboard=start_menu, resize_keyboard=True)

main_menu = [
    [InlineKeyboardButton(text="🔎 history", callback_data="history"),
     InlineKeyboardButton(text="📝 new chat", callback_data="new_chat")],
    [InlineKeyboardButton(text="create custom bot", callback_data="custom_bot"),
     InlineKeyboardButton(text="extension", callback_data="extension")],
    [InlineKeyboardButton(text=" settings", callback_data="settings")]
]
main_menu_kb = InlineKeyboardMarkup(inline_keyboard=main_menu)

settings_menu = [
    [InlineKeyboardButton(text="upgrade", callback_data="upgrade")],
    [InlineKeyboardButton(text="back", callback_data="back")]
]
settings_kd = InlineKeyboardMarkup(inline_keyboard=settings_menu, resize_keyboard=True)

custom_bot_menu = [
    [InlineKeyboardButton(text="set name", callback_data="set name")],
    [InlineKeyboardButton(text="base model", callback_data="base model")],
    [InlineKeyboardButton(text="system prompt", callback_data="system prompt")],
    [InlineKeyboardButton(text="submit", callback_data="submit")]
]
custom_bot_kb = InlineKeyboardMarkup(inline_keyboard=custom_bot_menu)

extension_menu = [
    [InlineKeyboardButton(text="projects", callback_data="projects")],
    [InlineKeyboardButton(text="add project", callback_data="add_project")],
    [InlineKeyboardButton(text="back", callback_data="back")]
]
extension_kb = InlineKeyboardMarkup(inline_keyboard=extension_menu)

upgrade_menu = [
    [InlineKeyboardButton(text="free", callback_data="free"),
     InlineKeyboardButton(text="basic", callback_data="basic"),
     InlineKeyboardButton(text="advanced", callback_data="advanced")],
    [InlineKeyboardButton(text="back", callback_data="back")]
]
upgrade_kb = InlineKeyboardMarkup(inline_keyboard=upgrade_menu)

"""
llm_menu = [
    [InlineKeyboardButton(text="ChatGPT", callback_data="free"),
     InlineKeyboardButton(text="basic", callback_data="basic"),
     InlineKeyboardButton(text="advanced", callback_data="advanced")],
    [InlineKeyboardButton(text="back", callback_data="back")]
]
llm_kb = InlineKeyboardMarkup(inline_keyboard=upgrade_menu)
"""


def make_row_keyboard(items: list[tuple[str, str]]):
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """

    row = [[InlineKeyboardButton(text=item[0], callback_data=item[1]) for item in items],
           [InlineKeyboardButton(text="cancel", callback_data="cancel")]]

    return InlineKeyboardMarkup(inline_keyboard=row, resize_keyboard=True)


def make_row_keyboard_1(items: list[str]):
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """

    row = [[InlineKeyboardButton(text=item, callback_data=item) for item in items],
           [InlineKeyboardButton(text="cancel", callback_data="cancel")]]

    return InlineKeyboardMarkup(inline_keyboard=row, resize_keyboard=True)


def make_history_keyboard(items: list[(str, str)]):
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """

    row = [[InlineKeyboardButton(text=item[0], callback_data=item[1]) for item in items],
           [InlineKeyboardButton(text="next", callback_data="next")],
           [InlineKeyboardButton(text="back", callback_data="back")]]

    return InlineKeyboardMarkup(inline_keyboard=row, resize_keyboard=True)


def make_history_keyboard_1(items: list[str]):
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """

    row = [[InlineKeyboardButton(text=item, callback_data=item) for item in items],
           [InlineKeyboardButton(text="next", callback_data="next")],
           [InlineKeyboardButton(text="back", callback_data="back")]]

    return InlineKeyboardMarkup(inline_keyboard=row, resize_keyboard=True)
