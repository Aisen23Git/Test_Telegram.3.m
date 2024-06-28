import asyncio
from aiogram import Bot
import logging

from config import bot, dp, database


async def on_startup(bot: Bot):
    await database.create_tables()


async def main():

    dp.startup.register(on_startup)
    # запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

# import asyncio
# from aiogram import Bot
# import logging
#
# from config import bot, dp, database
#
#
# from handlers import (
#     start_router,
#     order_router,
#     feedback_router,
#     picture_router,
#     echo_router,
#     survey_router
# )
#
#
# async def on_startup(bot: Bot):
#     await database.create_tables()
#
#
# async def main():
#     dp.include_router(picture_router)
#     dp.include_router(start_router)
#     dp.include_router(feedback_router)
#     dp.include_router(order_router)
#     dp.include_router(survey_router)
#
#     # в самом конце
#     dp.include_router(echo_router)
#
#     dp.startup.register(on_startup)
#     # запуск бота
#     await dp.start_polling(bot)
#
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())

import asyncio
from aiogram import Bot
import logging

from config import bot, dp, database
from db.database import Database


async def on_startup(bot: Bot):
    datab = Database('db.sqlite')
    await datab.create_table()


async def main():

    dp.startup.register(on_startup)
    # запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())