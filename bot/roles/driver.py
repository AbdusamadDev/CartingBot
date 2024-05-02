from aiogram import types
import logging
import asyncio

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
        # reply_markup=driver_my_loads_buttons(
        #     [
        #         (i["product_name"], i["id"], i["client"]["user"]["id"])
        #         for i in response["results"]
        #     ]
        # ),
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


async def driver_to_client_request_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    load_id = int(query.data.split(":")[-1])
    print("Load ID: ", load_id)
    load_object = get_one_load_details(token=token, load_id=load_id)
    if load_object["status_code"] != 200:
        await bot.send_message(query.message.chat.id, text=str(load_object))
        return
    load_object = load_object["message"]
    response = request_delivery(action="request_load", load_id=load_id, token=token)
    await bot.send_message(query.from_user.id, text=str(response))


# Callback Data: driver_successfully_delivered:<>
async def finished_delivery_request_to_client(query: types.CallbackQuery):
    load_id = query.data.split(":")[-1]
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    transaction = get_transaction(load_id)
    if transaction["status_code"] == 404:
        await bot.send_message(query.message.chat.id, text=str(transaction))
        return
    client_id = transaction["message"]["load"]["client"]["user"]["telegram_id"]
    transaction_uuid = transaction["message"]["uuid"]
    if client_id:
        load = get_one_load_details(token, load_id=load_id)
        await bot.send_message(
            chat_id=client_id,
            text=f"Your load {load} was delivered by {query.from_user.username}",
            reply_markup=client_confirmation_btn(transaction_uuid=transaction_uuid),
        )
    request = finished_delivery_request(token, transaction_id=transaction_uuid)
    await bot.send_message(chat_id=query.from_user.id, text=str(request))
