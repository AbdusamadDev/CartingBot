from aiogram import types
import logging

from bot.client import *
from bot.database import get_user_by_telegram_id
from bot.buttons import *
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


async def show_all_loads_for_driver(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    loads = get_all_loads_dispatcher(token)
    if loads["status_code"] == 200:
        loads = loads["message"]
        indices = [(load["id"], load["product_name"]) for load in loads]
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Requested fakely: {loads}",
            reply_markup=get_loads_for_driver(indices=indices),
        )


# async def proceed_driver_request_handler(query: types.CallbackQuery):
#     print("[INFO] Requesting driver load...")
#     load_id, client_id = query.data.split("_")[-2], query.data.split("_")[-1]
#     token = get_user_by_telegram_id(query.from_user.id)
#     if token:
#         token = token[2]
#     response = request_delivery(
#         token=token, load_id=load_id, user_id=client_id, action=""
#     )
#     await bot.send_message(
#         chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
#     )


async def driver_to_client_request_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    load_id = int(query.data.split(":")[-1])
    print(load_id)
    load_object = get_one_load_details(token=token, load_id=load_id)
    if load_object["status_code"] != 200:
        await bot.send_message(query.message.chat.id, text=str(load_object))
        return
    load_object = load_object["message"]
    client_id = load_object["client"]["user"]["id"]
    response = request_delivery(
        action="request_load", load_id=load_id, user_id=client_id, token=token
    )
    await bot.send_message(query.message.chat.id, text=str(response))


"""

{
    "receiver_phone_number": "+998940055555",
    "product_count": 55.0,
    "date_delivery": "2020-01-01T00:23:00+05:00",
    "product_name": "shkalat",
    "product_info": "ladshflkjahsdlkfjhasdfjkhasdlkf",
    "product_type": "kb",
    "from_location": [
        "e"
    ],
    "to_location": [
        "t"
    ],
    "address": "kjlhsdljfghsdfgsdfg",
    "status": "active",
    "product_image": "http://localhost:8000/media/load_images/5a661fb9-76d3-4bbd-8ec4-9f0163cd714f.jpg",
    "id": 1,
    "client": {
        "first_name": null,
        "last_name": null,
        "obj_status": "available",
        "user": {
            "phonenumber": "+998940056655",
            "user_type": "client",
            "first_name": null,
            "last_name": null,
            "id": 2
        }
    }
}
"""
