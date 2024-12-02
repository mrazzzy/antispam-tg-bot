from aiogram import Bot, Dispatcher
from config import Config


conf = Config()
bot = Bot(token=conf.get_token())
dp = Dispatcher()
