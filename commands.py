from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand


FILM_COMMAND = Command("films")
ADD_FILM_COMMAND = Command("add_film")

COMMANDS = [
    BotCommand(command="films", description="Показати всі фільми"),
    BotCommand(command="add_film", description="Додати новий фільм")
]