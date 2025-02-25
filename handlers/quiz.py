from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot

async def quiz(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Далее', callback_data='button1')

    keyboard.add(button)

    question = 'Какое время года?'
    answer = ['Зима', 'Весна', 'Лето','Осень']

    with open('media/IMG_2840.jpg', 'rb') as image:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=image)


    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation= ';-;',
        open_period=60,
        reply_markup=keyboard
    )

async def quiz_2(call: types.CallbackQuery):
    question = ['Dota 2 or CS:GO']
    answer = ['Dota 2', 'CS:GO']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=1,
    )




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(quiz, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='button1')
