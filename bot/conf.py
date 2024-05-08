from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types


# PRODUCTION

TOKEN="6998603334:AAEUXAIxN4aN9q3VfqYmAk90ZE0ER6m2i60"
DOMAIN = "https://new-api.carting.uz"


# DEVELOPMENT

# TOKEN = "6806518107:AAHKmoXl1OPVxPc2KaC4BamE3ZLVvnYQJL4"
# DOMAIN = "http://localhost:8000"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


