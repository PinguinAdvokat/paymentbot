import tools
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, 
                           InlineKeyboardButton, LabeledPrice, SuccessfulPayment, 
                           RefundedPayment, PreCheckoutQuery)
from aiogram.filters import Command
from user import ro


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
    if tools.is_user_in_database(username=pre_ch_query.from_user.username):
        await bot.answer_pre_checkout_query(pre_ch_query.id, ok=True)
    else:
        await bot.answer_pre_checkout_query(pre_ch_query.id, ok=False, error_message='Some error message...')


@dp.message(F.successful_payment)
async def process_successful_payment(message:Message):
    tools.add_balance(message.chat.id, message.invoice.total_amount / 100)
    await message.answer(f"Ваш баланс успешно пополнен на {message.invoice.total_amount / 100} рублей.\nВаш текущий баланс: *{tools.get_user_info(message.chat.id, 'balance')} рублей*")


async def bot_start():
    dp.include_routers(ro)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(bot_start())


if __name__=='__main__':
    asyncio.run(main())