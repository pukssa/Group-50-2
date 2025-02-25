# config
from aiogram import Bot, Dispatcher
from decouple import  config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


token = config("TOKEN")

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

Admins = [1193518366,]