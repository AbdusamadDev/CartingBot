from aiogram.dispatcher import FSMContext
from aiogram import types

from ..states import DeliveryRequestState
from ..main import dp, bot
from ..database import *
from ..buttons import *
from ..client import *


async def dispatcher_get_my_loads_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = dispatcher_get_my_loads(token)
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )


async def show_all_drivers_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    else:
        pass
    response = show_all_drivers(token=token)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=str(response),
    )


async def dispatcher_show_all_loads_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = get_all_loads_dispatcher(token)
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )


async def dispatcher_request_to_driver_handler(
    query: types.CallbackQuery, state: FSMContext
):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    context = await state.get_data()
    load_id = query.data.split("_")[-1]
    driver_id = context["driver_id"]
    response = request_delivery(token=token, load_id=load_id, user_id=driver_id)
    await query.answer(str(response))


async def request_for_load(query: types.CallbackQuery, state: FSMContext):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = show_all_drivers(token=token)
    driver_data = [
        (i["user"]["id"], f"{i['first_name']} {i['last_name']}") for i in response
    ]
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"Choose driver to : {response}",
        reply_markup=get_driver_buttons(driver_data),
    )


async def ask_for_which_load_handler(query: types.CallbackQuery, state: FSMContext):
    driver_id = query.data.split("_")[-1]
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    await state.update_data(driver_id=driver_id)
    loads = get_all_loads_dispatcher(token=token)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"Choose load to : {driver_id}",
        reply_markup=get_loads_button(indices=[i["id"] for i in loads["results"]]),
    )
    await DeliveryRequestState.load_id.set()
