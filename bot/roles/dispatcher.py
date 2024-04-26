from aiogram.dispatcher import FSMContext
from aiogram import types

from ..states import DeliveryRequestState
from ..main import dp, bot
from ..database import *
from ..buttons import *
from ..client import *


@dp.callback_query_handler(lambda c: c.data == "dispatcher_show_all_loads")
async def dispatcher_show_all_loads_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = get_all_loads_dispatcher(token)
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )


@dp.callback_query_handler(lambda c: c.data == "dispatcher_show_drivers")
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


@dp.callback_query_handler(lambda c: c.data == "dispatcher_get_my_loads")
async def dispatcher_get_my_loads_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = dispatcher_get_my_loads(token)
    print("Dispatcher response: ", response)
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )


@dp.callback_query_handler(lambda c: c.data == "request_dispatcher_to_driver")
async def request_for_load(query: types.CallbackQuery, state: FSMContext):
    load_id = query.data.split("_")[-1]
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    await DeliveryRequestState.load_id.set()
    await state.set_state(DeliveryRequestState.load_id)
    await state.update_data(load_id=load_id)
    print(token)
    response = show_all_drivers(token=token)

    # Extract driver ID and full name from response
    driver_data = [
        (i["user"]["id"], f"{i['first_name']} {i['last_name']}") for i in response
    ]
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"Choose driver to : {response}",
        reply_markup=get_driver_buttons(driver_data),
    )
