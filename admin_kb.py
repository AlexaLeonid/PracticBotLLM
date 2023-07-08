from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove


admin_menu = [
    [InlineKeyboardButton(text="view statistics", callback_data="view_statistics"),
     InlineKeyboardButton(text="change limits", callback_data="change_limits")],
    [InlineKeyboardButton(text="grant privileges", callback_data="grant_privileges")]
]
start_kd = InlineKeyboardMarkup(inline_keyboard=admin_menu, resize_keyboard=True)
