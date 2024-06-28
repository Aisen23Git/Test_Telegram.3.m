from aiogram import Router, types
import asyncio

echo_router = Router()


@echo_router.message()
async def echo(message: types.Message):
    # logging.info(message)
    reversed_text = ' '.join(message.text.split()[::-1])
    await message.answer(reversed_text, "Я не понимаю вас, поробуйте следующие команды: \n"
    "/start - начать диалог\n""/picture - отправить картинку")

