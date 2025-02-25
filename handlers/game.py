from aiogram import types, Dispatcher
#from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from random import choice
games = ['⚽', '️🎰', '🏀', '🎯', '🎳', '🎲']
async def game_ (message: types.Message):
    game = choice(games)
    await bot.send_dice(
        emoji=game,
        chat_id = message.chat.id,
    )
def register_game(dp: Dispatcher):
    dp.register_message_handler(game_, commands=['game_dice'])