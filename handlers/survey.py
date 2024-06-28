from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db.database import Database
from db.queries import Queries
from config import database


survey_router = Router()


db = Database("survey_data.db")


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary = State()


@survey_router.message(Command(commands="start_survey"))
async def start_survey(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(BookSurvey.name)


@survey_router.message(BookSurvey.name)
async def ask_age(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(BookSurvey.age)


@survey_router.message(BookSurvey.age)
async def ask_occupation(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 17:
            await message.answer("Опрос прекращен, так как возраст меньше 17 лет.")
            await state.clear()
            return
        await state.update_data(age=age)
        await message.answer("Какой у вас род занятий?")
        await state.set_state(BookSurvey.occupation)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение возраста.")


@survey_router.message(BookSurvey.occupation)
async def ask_salary(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    await message.answer("Какова ваша заработная плата?")
    await state.set_state(BookSurvey.salary)


@survey_router.message(BookSurvey.salary)
async def finish_survey(message: types.Message, state: FSMContext):
    try:
        salary = float(message.text)
        data = await state.get_data()
        data['salary'] = salary

        await db.execute(Queries.INSERT_SURVEY_DATA, (data['name'], data['age'], data['occupation'], data['salary']))

        await state.clear()
        await message.answer("Спасибо за прохождение опроса!")
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение заработной платы.")

@survey_router.message(Command(commands="stop"))
@survey_router.message(F.text.casefold() == "стоп")
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за прохождение опроса!")

# Тут были сомнения и дальнейшие изменения сверху

# class BookSurvey(StatesGroup):
#     name = State()
#     age = State()
#     occupation = State()
#     salary = State()
#
#
# @survey_router.message(Command("opros"))
# async def start_survey(message: types.Message, state: FSMContext):
#     #Устанавливаем состояние
#     await state.set_state(BookSurvey.name)
#     await message.answer("Как вас зовут ?")
#
#
# @survey_router.message(Command("stop"))
# @survey_router.message(F.text.lower() == "стоп")
# async def stop(message: types.Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Спасибо за прохождение опроса!")
#
#
# @survey_router.message(BookSurvey.name)
# async def process_name(message: types.Message, state: FSMContext):
#     print("Message:",message.text)
#     #Сохраняем данные пользователя
#     await state.update_data(name = message.text)
#
#     #Устанавливаем состояние
#     await state.set_state(BookSurvey.age)
#     await message.answer("Сколько вам лет?")
#
#
# @survey_router.message(BookSurvey.age)
# async def process_age(message: types.Message, state: FSMContext):
#     age = message.text
#     if not age.isdigit():
#         await message.answer("Пожалуйста введите только цифры !")
#         return
#     age = int(age)
#     if age <10 or age > 90:
#         await message.answer("Введите возраст от 10 до 90 !")
#         return
#     # elif age >18:
#     #     pass
#
#     # Сохраняем данные пользователя
#     await state.update_data(age = message.text)
#
#     # Устанавливаем состояние
#     await state.set_state(BookSurvey.occupation)
#     await message.answer("Какой выш род деятельности?")
#
#
# @survey_router.message(BookSurvey.occupation)
# async def process_gender(message: types.Message, state: FSMContext):
#     # Сохраняем данные пользователя
#     await state.update_data(occupation = message.text)
#
#     # Устанавливаем состояние
#     await state.set_state(BookSurvey.salary)
#     await message.answer("Какая у вас зарплата?")
#
#
# @survey_router.message(BookSurvey.salary)
# async def process_favorite_food(message: types.Message, state: FSMContext):
#     # Сохраняем данные пользователя
#     await state.update_data(salary = message.text)
#
#     # Берем сохраненные данные
#     data = await state.get_data()
#     print("Data", data)
#     # Save to DB
#     await database.execute("""
#         INSERT INTO survey_results (name, age, occupation, salary)
#         VALUES (?, ?, ?, ?)""",
#         data['name'], data['age'], data['occupation'], data['salary']
#     )
#     # Чистим данные
#     await state.clear()
#     await message.answer("Спасибо за прохождение опроса?")



