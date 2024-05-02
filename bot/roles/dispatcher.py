from bot.client import dispatcher_get_my_loads
from aiogram.dispatcher import FSMContext
from bot.conf import bot
from bot.database import *
from bot.client import *
from bot.states import *
from bot.buttons import *
from aiogram import types


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
    if response["status_code"] == 200:
        response = response["message"]
        print(response)
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Requested fakely: {response}",
            reply_markup=get_loads_for_driver(
                [(i["id"], i["product_name"]) for i in response["results"]]
            ),
        )


async def dispatcher_request_to_driver_handler(
    query: types.CallbackQuery, state: FSMContext
):
    print("[INFO] Requesting to driver")
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    context = await state.get_data()
    load_id = query.data.split("_")[-1]
    driver_id = context["driver_id"]
    response = request_delivery(
        token=token, load_id=load_id, user_id=driver_id, action="request_transaction"
    )
    await query.answer(str(response))


async def ask_for_which_load_handler(query: types.CallbackQuery, state: FSMContext):
    print("[INFO] Choosing load from loads list")
    driver_id = query.data.split("_")[-1]
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    await state.update_data(driver_id=driver_id)
    loads = get_all_loads_dispatcher(token=token)
    if loads["status_code"] == 200:
        loads = loads["message"]
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Choose load to : {driver_id}",
            reply_markup=get_loads_button(
                indices=[(i["id"], i["product_name"]) for i in loads["results"]]
            ),
        )
        await DeliveryRequestState.load_id.set()


async def request_for_load_profile_view(query: types.CallbackQuery, state: FSMContext):
    print("[INFO] Profile view handler here...")
    driver_id = int(query.data.split(":")[-1])
    async with state.proxy() as data:
        data["driver_id"] = driver_id
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    print(driver_id, type(driver_id))
    driver_details = get_driver_details(token=token, driver_id=driver_id)
    car_details = get_drivers_car_details(driver_id=driver_id)
    print(driver_details)
    print(car_details)
    if driver_details["status_code"] == 200:
        driver_details = driver_details["message"]
        message = f"👤 Fullname: {driver_details['first_name']} {driver_details['last_name']}\n📞 Phone number: {driver_details['user']['phonenumber']}"
        if car_details["status_code"] != 404:
            car_details = car_details["message"]
            message += f"\n🚗 Car model: {car_details['model']}\n🚗 Car number: {car_details['number']}"
        await bot.send_message(
            query.message.chat.id,
            text=message,
            reply_markup=get_one_driver_button(driver_id=driver_id),
        )


async def request_for_load(query: types.CallbackQuery, state: FSMContext):
    print("Fetching drivers list")
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = show_all_drivers(token=token)
    driver_data = [(i["id"], f"{i['first_name']} {i['last_name']}") for i in response]
    await bot.send_message(
        chat_id=query.message.chat.id,
        text="Please choose one of the drivers and review the details of the driver.",
        reply_markup=get_driver_buttons(driver_data),
    )


