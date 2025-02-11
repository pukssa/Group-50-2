from aiogram import types, Dispatcher, Bot, executor
from decouple import config
import logging

token = config("TOKEN")

bot = Bot(token=token)
dp = Dispatcher(bot)
admins = [1193518366,]


@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}!\n'
                           f'Твой Telegam ID - {message.from_user.id}\n')
    await message.answer('Привет мир')


@dp.message_handler(commands="meme")
async def meme_handler(message: types.Message):
    with open('media/IMG_2840.jpg', 'rb') as image:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=image)


@dp.message_handler()
async def echo_or_square(message: types.Message):
    try:
        number = float(message.text)
        await message.answer(str(number ** 2))
    except ValueError:
        await message.answer(message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)