import tools
import asyncio
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery


ro = Router(name=__name__)


@ro.message(CommandStart())
async def start_mes(message:Message):
    tools.create_user(message.chat.id, message.from_user.username, balance=100)
    await message.answer('hello world!')