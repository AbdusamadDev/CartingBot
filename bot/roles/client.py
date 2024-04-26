from aiogram.dispatcher import FSMContext
from aiogram import types

from ..states import DeliveryRequestState
from ..main import dp, bot
from ..database import *
from ..buttons import *
from ..client import *




@dp.callback_query_handler(lambda c: c.data == "show_my_load")
async def client_show_my_load_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = get_client_personal_loads(token)
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )


