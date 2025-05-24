import os
import logging
import asyncio
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message

from routes import films_router
from commands import COMMANDS


load_dotenv()

FBOT = os.getenv("FBOT")
dp = Dispatcher()
dp.include_routers(films_router)

@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text=f"Привіт {message.from_user.full_name}!")

async def main():
    bot = Bot(token=FBOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())