import tools
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, 
                           InlineKeyboardButton, LabeledPrice, SuccessfulPayment, 
                           RefundedPayment, PreCheckoutQuery)
from aiogram.filters import Command
from handlers import ro


bot = Bot(tools.get_data_json('bot_token'))
dp = Dispatcher()

#payment
@dp.message(Command('pay'))
async def pay(message:Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='100 руб.', callback_data='pay_100')],
        [InlineKeyboardButton(text='200 руб.', callback_data='pay_200')],
        [InlineKeyboardButton(text='300 руб.', callback_data='pay_300')],
        [InlineKeyboardButton(text='400 руб.', callback_data='pay_400')],
        [InlineKeyboardButton(text='500 руб.', callback_data='pay_500')]        
    ])
    await message.answer('Выберите сумму на которую вы хотите пополнить баланс', reply_markup=kb)


@dp.callback_query(lambda c: c.data[:3] == 'pay')
async def callback_pay(callback:CallbackQuery):
    await bot.send_invoice(
        chat_id= callback.message.chat.id,
        title="пополнение",
        description="пополнение баланса с которого будут списываться деньги за ежемесечный тариф",
        payload=f'пополнение баланса',
        provider_token=tools.get_data_json('payment_token'),
        currency='RUB',
        prices=[
            LabeledPrice(
                label='пополнение баланса',
                amount=int(callback.data[4:]) * 100
            )
        ],
        start_parameter=f'testpaymentbot',
        request_timeout=30
    )
    

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_ch_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_ch_query.id,  ok=True)


@dp.message(F.successful_payment)
async def process_successful_payment(message:Message):
    await message.answer(f'баланс пользователя {message.from_user.username} успешно пополнен')


async def bot_start():
    dp.include_routers(ro)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(bot_start())


if __name__=='__main__':
    asyncio.run(main())