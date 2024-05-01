from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import os

TOKEN="6998603334:AAEUXAIxN4aN9q3VfqYmAk90ZE0ER6m2i60"
DOMAIN="https://new-api.carting.uz"
BASE_DIR = os.path.join("C:/Users/Abdusamad/Documents/Backend/carting.uz-bot/")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
