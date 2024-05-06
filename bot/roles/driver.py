from aiogram import types

from bot.client import *
from bot.buttons import *
from bot.tests import data
from bot.conf import bot
from bot.utils import *


async def show_my_loads(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    response = get_my_loads(token=token)

    message = "Your loads:\n"
    load_buttons = []

    for index, load in enumerate(data["results"], start=1):
        load_details = f"📦 {load['product_name']}\n📅 {load['date_delivery']}\n📌 From: {', '.join(load['from_location'])}\n📌 To: {', '.join(load['to_location'])}\n\n"
        message += load_details
        button_text = f"Load {index}"
        load_buttons.append(    
            types.InlineKeyboardButton(
                text=button_text, callback_data=f"load_details:{load['id']}"
            )
        )

    keyboard = types.InlineKeyboardMarkup(row_width=7)
    keyboard.add(*load_buttons)

    await bot.send_message(
        chat_id=query.message.chat.id, text=message, reply_markup=keyboard
    )


async def load_details_callback(query: types.CallbackQuery):
    callback_data = query.data.split(":")
    load_id = int(callback_data[-1])

    token = await authenticate(bot, query.from_user.id)
    load_details = get_one_load_details(token=token, load_id=load_id)
    print(load_details)
    message = f"Load ID: {load_details['id']}\n"
    message += f"Product Name: {load_details['product_name']}\n"
    message += f"Date Delivery: {load_details['date_delivery']}\n"
    message += f"From: {', '.join(load_details['from_location'])}\n"
    message += f"To: {', '.join(load_details['to_location'])}\n"
    message += f"Address: {load_details['address']}\n"
    message += f"Status: {load_details['status']}\n"
    await bot.send_message(chat_id=query.message.chat.id, text=message)


async def show_all_loads_for_driver(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    loads = get_all_loads_dispatcher(token)
    if loads["status_code"] == 200:
        loads = loads["message"]["results"]
        indices = [load["id"] for load in loads]
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="",
            reply_markup=get_loads_for_driver(indices=indices),
        )
    else:
        await query.message.answer("Loads does not exist in backend.")


async def driver_to_client_request_handler(query: types.CallbackQuery):
    token = await authenticate(bot, token)
    load_id = int(query.data.split(":")[-1])
    print("Load ID: ", load_id)
    load_object = get_one_load_details(token=token, load_id=load_id)
    if load_object["status_code"] != 200:
        await bot.send_message(query.message.chat.id, text=str(load_object))
        return
    load_object = load_object["message"]
    response = request_delivery(action="request_load", load_id=load_id, token=token)
    await bot.send_message(query.from_user.id, text=str(response))


async def finished_delivery_request_to_client(query: types.CallbackQuery):
    load_id = query.data.split(":")[-1]
    token = await authenticate(bot, query.from_user.id)
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
            text=f"Sizning yukingiz: {load} {query.from_user.username} tomonidan yetqazib berildi!",
            reply_markup=client_confirmation_btn(transaction_uuid=transaction_uuid),
        )
    request = finished_delivery_request(token, transaction_id=transaction_uuid)
    await bot.send_message(chat_id=query.from_user.id, text=str(request))
