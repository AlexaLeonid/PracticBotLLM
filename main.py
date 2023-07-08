import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
import handlers
import admin_handlers
import creating_custom_bot
import creating_new_chat
import creating_project


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(creating_custom_bot.router)
    dp.include_router(creating_new_chat.router)
    dp.include_router(creating_project.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
