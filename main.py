import os
import logging
import asyncio
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import data
from keyboards import films_keyboard_markup
from commands import FILM_COMMAND

load_dotenv()

FBOT = os.getenv("FBOT")
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text=f"Привіт {message.from_user.full_name}!")

@dp.message(FILM_COMMAND)
async def get_films(message: Message):
    films = data.get_films()
    keyboard = films_keyboard_markup(films)
    await message.answer(
        text="Список наявних фільмів:",
        reply_markup=keyboard
    )

async def main():
    bot = Bot(token=FBOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())