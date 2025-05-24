from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand


FILM_COMMAND = Command("films")

COMMANDS = [
    BotCommand(command="films", description="Показати всі фільми")
]