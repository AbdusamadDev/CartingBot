from aiogram.dispatcher import FSMContext
from aiogram import types

from bot.client import *
from bot.buttons import *
from bot.conf import bot
from bot.utils import *


# async def show_my_loads(query: types.CallbackQuery):
#     page = 1
#     token = await authenticate(bot, query.from_user.id)
#     response = get_my_loads(token=token, page=page)
#     if response["status_code"] == 200:
#         response =
#         await send_paginated_load_details(query.message.chat.id, response, page)
#     else:
#         await query.message.answer("Sizda hali yuklar yo'q")


# async def load_pagination_callback(query: types.CallbackQuery):
#     action, current_page = query.data.split(":")[1:]
#     current_page = int(current_page)
#     if action == "next":
#         next_page = current_page + 1
#     elif action == "previous":
#         next_page = current_page - 1
#     else:
#         return
#     token = await authenticate(bot, query.from_user.id)
#     response = get_my_loads(token=token, page=next_page)
#     if response["status_code"] == 200:
#         await send_paginated_load_details(query.message.chat.id, response, next_page)
#     else:
#         await query.message.answer("Sizda hali yuklar yo'q")


# async def send_paginated_load_details(chat_id, response, current_page):
#     if response["status_code"] == 200:
#         loads = response["message"]
#         num_per_page = 10
#         start_index = (current_page - 1) * num_per_page
#         end_index = min(start_index + num_per_page, len(loads))
#         print(loads)
#         print(start_index, end_index)
#         loads_page = loads[start_index:end_index]
#         message_text = "\n\n".join([str(load) for load in loads_page])
#         pagination_markup = generate_pagination_buttons(
#             current_page, len(loads), num_per_page
#         )
#         await bot.send_message(
#             chat_id=chat_id,
#             text=message_text,
#             reply_markup=pagination_markup,
#         )
#     else:
#         await bot.send_message(chat_id=chat_id, text="Failed to fetch loads")


# def generate_pagination_buttons(current_page, total_count, num_per_page):
#     total_pages = (total_count + num_per_page - 1) // num_per_page
#     buttons = []
#     if current_page > 1:
#         buttons.append(
#             types.InlineKeyboardButton(
#                 text="<< Previous",
#                 callback_data=f"load_pagination:previous:{current_page}",
#             )
#         )
#     if current_page < total_pages:
#         buttons.append(
#             types.InlineKeyboardButton(
#                 text="Next >>", callback_data=f"load_pagination:next:{current_page}"
#             )
#         )
#     return types.InlineKeyboardMarkup().add(*buttons)


async def show_my_loads(query: types.CallbackQuery):
    page = 1
    token = await authenticate(bot, query.from_user.id)
    response = get_my_loads(token=token, page=page)
    print("Sending paginated response")
    await send_paginated_load_details(query.message.chat.id, response)


async def load_pagination_callback(query: types.CallbackQuery):
    action, current_page = query.data.split(":")[1:]
    current_page = int(current_page)
    print(action)
    print(current_page)

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
    message_text = str(loads)
    pagination_markup = generate_pagination_buttons(
        current_page, response["message"]["previous"], response["message"]["next"]
    )

    if message_id:
        # Update existing message
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=message_text,
            reply_markup=pagination_markup,
        )
    else:
        # Send new message
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=pagination_markup,
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
    return types.InlineKeyboardMarkup().add(*buttons)


async def load_details_callback(query: types.CallbackQuery):
    callback_data = query.data.split(":")
    load_id = int(callback_data[-1])

    token = await authenticate(bot, query.from_user.id)
    load_details = get_one_load_details(token=token, load_id=load_id)
    if load_details["status_code"] == 200:
        load_details = load_details["message"]
        message = f"Load ID: {load_details['id']}\n"
        message += f"Product Name: {load_details['product_name']}\n"
        message += f"Date Delivery: {load_details['date_delivery']}\n"
        message += f"From: {', '.join(load_details['from_location'])}\n"
        message += f"To: {', '.join(load_details['to_location'])}\n"
        message += f"Address: {load_details['address']}\n"
        message += f"Status: {load_details['status']}\n"
        await bot.send_message(chat_id=query.message.chat.id, text=message)
    else:
        await query.message.answer("Yuk mavjud emas")


async def show_all_loads_for_driver(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    loads = get_all_loads_dispatcher(token)
    if loads["status_code"] == 200:
        loads = loads["message"]["results"]
        indices = [load["id"] for load in loads]
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=str(loads),
            reply_markup=get_loads_for_driver(indices=indices),
        )
    else:
        await query.message.answer("Loads does not exist in backend.")


async def driver_to_client_request_handler(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    print(query.data)
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
