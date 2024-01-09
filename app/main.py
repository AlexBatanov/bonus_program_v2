import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from hendlers.start import start_router
from hendlers.users import user_router
from hendlers.buyers import buyer_router
from hendlers.bonus_points import bonus_router
from hendlers.reports import reports_router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

from db.models import BonusPoint

bonus = BonusPoint(name='ss')



async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.include_router(start_router)
    dp.include_router(bonus_router)
    dp.include_router(user_router)
    dp.include_router(buyer_router)
    dp.include_router(reports_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot exit')