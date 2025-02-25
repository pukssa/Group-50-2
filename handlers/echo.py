# echo
from aiogram import types, Dispatcher


# @dp.message_handler()
async def echo_or_square(message: types.Message):
    try:
        number = float(message.text)
        await message.answer(str(number ** 2))
    except ValueError:
        await message.answer(message.text)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_or_square)