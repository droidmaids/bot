from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from commands import FILM_COMMAND, ADD_FILM_COMMAND
import data
from keyboards import films_keyboard_markup, FilmCallback, del_film_keyboard
from models import FilmModel
from forms import FilmForm

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
    film_data = data.get_films(film_id=callback_data.id)
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
            ),
            reply_markup=del_film_keyboard(callback_data.id)
    )



@films_router.message(ADD_FILM_COMMAND)
async def add_film(message: Message, state: FSMContext):
    await state.set_state(FilmForm.name)
    await message.answer(
        text="Введіть назву фільму",
        reply_markup=ReplyKeyboardRemove()
    )


@films_router.message(FilmForm.name)
async def get_film_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer(
        text="Введіть опис для фільму.",
        reply_markup=ReplyKeyboardRemove()
    )


@films_router.message(FilmForm.description)
async def get_film_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer(
        text="Введіть рейтинг фільму від 0 до 18.",
        reply_markup=ReplyKeyboardRemove()
    )


@films_router.message(FilmForm.rating)
async def get_film_rating(message: Message, state: FSMContext):
    await state.update_data(rating=float(message.text))
    await state.set_state(FilmForm.genre)
    await message.answer(
        text="Введіть жанр фільму.",
        reply_markup=ReplyKeyboardRemove()
    )


@films_router.message(FilmForm.genre)
async def get_film_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer(
        text="Введіть акторів фільму через кому та пробіл ', '",
        reply_markup=ReplyKeyboardRemove()
    )


@films_router.message(FilmForm.actors)
async def get_film_actors(message: Message, state: FSMContext):
    await state.update_data(actors=message.text.split(", "))
    await state.set_state(FilmForm.poster)
    await message.answer(
        text="Вставте покликання на постер фільму.",
        reply_markup=ReplyKeyboardRemove()
    )

@films_router.message(FilmForm.poster)
async def get_film_poster(message: Message, state: FSMContext):
    film_data = await state.update_data(poster=message.text)
    data.add_film(film_data)
    await state.clear()
    await message.answer(
        text=f"Фільм '{film_data["name"]}' успішно додано.",
        reply_markup=ReplyKeyboardRemove()
    )


@films_router.callback_query(F.data.startswith("del_film_"))
async def del_film(callback: CallbackQuery, state: FSMContext):
    film_id = int(callback.data.split("_")[-1])
    film = data.get_films(film_id = film_id)
    data.delete_file(film_id)
    await callback.message.answer(
        text=f"Фільм '{film.get("name")}' успішно видалено!"
    )