from aiogram import Router
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove

from commands import FILM_COMMAND
import data
from keyboards import films_keyboard_markup, FilmCallback
from models import FilmModel

films_router = Router()


@films_router.message(FILM_COMMAND)
async def get_films(message: Message):
    films = data.get_films()
    keyboard = films_keyboard_markup(films)
    await message.answer(
        text="Список наявних фільмів:",
        reply_markup=keyboard
    )

@films_router.callback_query(FilmCallback.filter())
async def get_film(callback: CallbackQuery, callback_data: FilmCallback):
    film_data = data.get_films(callback_data.id)
    film = FilmModel(**film_data)
    text = f"""
    Фільм: {film.name}
    Опис: {film.description}
    Рейтинг: {film.rating} 
    Жанр: {film.genre}
    Актори: {",".join(film.actors)}   
    """
    await callback.message.answer_photo(
            caption=text,
            photo=URLInputFile(
                url=film.poster,
                filename=film.name
            )
    )