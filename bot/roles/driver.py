from aiogram import types
import logging

from bot.client import get_my_loads, request_delivery
from bot.database import get_user_by_telegram_id
from bot.buttons import driver_my_loads_buttons
from bot.conf import bot


async def show_my_loads(query: types.CallbackQuery):
    logging.info("Attempting to send personal loads...")
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = get_my_loads(token=token)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=str(response),
        reply_markup=driver_my_loads_buttons(
            [
                (i["product_name"], i["id"], i["client"]["user"]["id"])
                for i in response["results"]
            ]
        ),
    )


async def proceed_driver_request_handler(query: types.CallbackQuery):
    print("[INFO] Requesting driver load...")
    load_id, client_id = query.data.split("_")[-2], query.data.split("_")[-1]
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = request_delivery(
        token=token, load_id=load_id, user_id=client_id, action="request_load"
    )
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )



async def driver_to_client_request_handler(query: types.CallbackQuery):
    
    pass