import tools
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import message
from handlers import ro


bot = Bot(tools.get_data_json('bot_token'))
dp = Dispatcher()


async def bot_start():
    dp.include_routers(ro)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(bot_start())


if __name__=='__main__':
    asyncio.run(main())