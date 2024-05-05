from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import os

TOKEN="6806518107:AAHKmoXl1OPVxPc2KaC4BamE3ZLVvnYQJL4"
DOMAIN="https://new-api.carting.uz"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
