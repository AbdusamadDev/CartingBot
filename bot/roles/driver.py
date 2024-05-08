from aiogram.dispatcher import FSMContext
from aiogram import types

from bot.client import *
from bot.buttons import *
from bot.conf import bot
from bot.utils import *


async def show_my_loads(query: types.CallbackQuery):
    page = 1
    token = await authenticate(bot, query.from_user.id)
    response = get_my_loads(token=token, page=page)
    await send_paginated_load_details(query.message.chat.id, response)


async def load_pagination_callback(query: types.CallbackQuery):
    action, current_page = query.data.split(":")[1:]
    current_page = int(current_page)

    if action == "next":
        next_page = current_page + 1
    elif action == "previous":
        next_page = current_page - 1
    else:
        return

    token = await authenticate(bot, query.from_user.id)
    response = get_my_loads(token=token, page=next_page)
    await send_paginated_load_details(
        query.message.chat.id,
        response,
        current_page=next_page,
        message_id=query.message.message_id,
    )


async def send_paginated_load_details(
    chat_id, response, current_page=1, message_id=None
):
    loads = response["message"]["results"]
    indices = [load.get("id") for load in loads]
    indices = [index for index in indices if index is not None]
    message_text = ""
    print(loads)
    markup = InlineKeyboardMarkup(row_width=10)
    butt = []
    for index, data in enumerate(loads, start=1):
        message_text += f"{index}. {status[data['load']['status']]} {data['load']['product_name']}\n\n"
        butt.append(
            types.InlineKeyboardButton(
                text=str(index),
                callback_data=f"load_details:{data['load']['id']}:{data['uuid']}",
            )
        )
    pagination_markup = generate_pagination_buttons(
        current_page, response["message"]["previous"], response["message"]["next"]
    )
    markup.add(*butt)
    markup.add(*pagination_markup)
    if message_id:
        # Update existing message
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=message_text,
            reply_markup=markup,
        )
    else:
        # Send new message
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=markup,
        )


# Helper function to generate pagination buttons
def generate_pagination_buttons(current_page, previous, next):
    buttons = []
    if previous:
        buttons.append(
            types.InlineKeyboardButton(
                text="<< Previous",
                callback_data=f"load_pagination:previous:{current_page - 1}",
            )
        )
    if next:
        buttons.append(
            types.InlineKeyboardButton(
                text="Next >>", callback_data=f"load_pagination:next:{current_page + 1}"
            )
        )
    return buttons


async def load_details_callback(query: types.CallbackQuery):
    callback_data = query.data.split(":")
    print(callback_data)
    load_id, transaction_id = callback_data[1:]

    token = await authenticate(bot, query.from_user.id)
    load_details = get_one_load_details(token=token, load_id=int(load_id))
    if load_details["status_code"] == 200:
        load_details = load_details["message"]
        message = f"Load ID: {load_details['id']}\n"
        message += f"Product Name: {load_details['product_name']}\n"
        message += f"Date Delivery: {load_details['date_delivery']}\n"
        message += f"From: {', '.join(load_details['from_location'])}\n"
        message += f"To: {', '.join(load_details['to_location'])}\n"
        message += f"Address: {load_details['address']}\n"
        message += f"Status: {load_details['status']}\n"
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=message,
            reply_markup=(
                None
                if load_details["status"] != "process"
                else successfully_delivered_btn(transaction_id)
            ),
        )
    else:
        await query.message.answer("Yuk mavjud emas")


async def show_all_loads_for_driver(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    loads_response = get_all_loads_dispatcher(token)

    if loads_response["status_code"] == 200:
        loads = loads_response["message"]["results"]
        message_text = ""
        buttons = []
        for load in loads:
            index = load["id"]
            load_name = load["product_name"]
            message_text += f"{index}. {load_name}\n\n"
            button_text = str(index)
            callback_data = f"load_preview:{index}"
            buttons.append(
                types.InlineKeyboardButton(
                    text=button_text, callback_data=callback_data
                )
            )

        reply_markup = types.InlineKeyboardMarkup(row_width=10).add(*buttons)
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=message_text,
            reply_markup=reply_markup,
        )
    else:
        await query.message.answer("Loads do not exist in the backend.")


async def load_preview(query: types.CallbackQuery):
    load_id = query.data.split(":")[1]  # Extracting load ID from the callback data
    token = await authenticate(bot, query.from_user.id)
    load_details_response = get_one_load_details(token, load_id)

    if load_details_response["status_code"] == 200:
        load_details = load_details_response["message"]
        # Construct a decorative message with load details
        message_text = f"<b>Load Details:</b>\n\n"
        message_text += f"<b>Name:</b> {load_details['product_name']}\n"
        message_text += f"<b>Info:</b> {load_details['product_info']}\n"
        message_text += f"<b>Count:</b> {load_details['product_count']}\n"
        message_text += f"<b>Type:</b> {load_details['product_type']}\n"
        message_text += f"<b>Status:</b> {load_details['status']}\n"
        message_text += (
            f"<b>From Location:</b> {', '.join(load_details['from_location'])}\n"
        )
        message_text += (
            f"<b>To Location:</b> {', '.join(load_details['to_location'])}\n"
        )
        message_text += f"<b>Delivery Date:</b> {load_details['date_delivery']}\n"
        markup = InlineKeyboardMarkup(row_width=5)
        markup.add(
            InlineKeyboardButton(
                text="Shu yukni olish",
                callback_data=f"driver_request_to_client:{load_id}",
            )
        )
        # Send the decorative message
        await query.message.answer(
            text=message_text, parse_mode="HTML", reply_markup=markup
        )
    else:
        await query.message.answer("Load details could not be retrieved.")


async def driver_to_client_request_handler(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    print(query.data)
    load_id = int(query.data.split(":")[-1])
    print("Load ID: ", load_id)
    load_object = get_one_load_details(token=token, load_id=load_id)
    if load_object["status_code"] != 200:
        await bot.send_message(query.message.chat.id, text="Ma'lumot topilmadi")
        return
    load_object = load_object["message"]
    response = request_delivery(action="request_load", load_id=load_id, token=token)
    if "success" in str(response):
        await bot.send_message(
            query.from_user.id, text="So'rovingiz mijozga yuborildi!"
        )
    else:
        await query.message.answer("Xatolik yuz berdi!")


async def finished_delivery_request_to_client(query: types.CallbackQuery):
    load_id = query.data.split(":")[-1]
    token = await authenticate(bot, query.from_user.id)
    transaction = get_transaction(load_id)
    if transaction["status_code"] == 404:
        await bot.send_message(query.message.chat.id, text="Malumot topilmadi!")
        return
    client_id = transaction["message"]["load"]["client"]["user"]["telegram_id"]
    transaction_uuid = transaction["message"]["uuid"]
    if client_id:
        load = get_one_load_details(token, load_id=load_id)
        await bot.send_message(
            chat_id=client_id,
            text=f"Sizning yukingiz: {load['message']['product_name']} {query.from_user.username} tomonidan yetqazib berildi!",
            reply_markup=client_confirmation_btn(transaction_uuid=transaction_uuid),
        )
    request = finished_delivery_request(token, transaction_id=transaction_uuid)
    if request["status_code"] == 200:
        await bot.send_message(
            chat_id=query.from_user.id,
            text="Tabriklaymiz, yukni yetkazib berildi va mijoz tomonidan tasdiqlandi!",
        )
    else:
        await query.message.answer("Xatolik yuz berdi!")
