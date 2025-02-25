# commands.py
from aiogram import types, Dispatcher
from config import bot
import buttons


async def start_hanler(message: types.Message):
    print('Обработчик старта')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}\n'
                                f'Твой Telegram ID - {message.from_user.id}\n', reply_markup=buttons.start)

    await message.answer('Привет мир')


async def mem_handler(message: types.Message):
    # photo = open('media/images.jpeg', 'rb')

    with open('media/images.jpeg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_hanler, commands=['start'])
    dp.register_message_handler(mem_handler, commands=['mem'])