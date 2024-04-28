from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor, Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from conf import TOKEN
from client import *
from buttons import *
from database import *
import logging
import re

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
auth_token = None
create_table()


class RegistrationState(StatesGroup):
    fullname = State()
    phonenumber = State()
    sms_code = State()
    role = State()
    password = State()


class LoadCreationState(StatesGroup):
    product_name = State()
    product_info = State()
    product_type = State()
    product_count = State()
    address = State()
    receiver_phone_number = State()
    date_delivery = State()


class DeliveryRequestState(StatesGroup):
    driver_id = State()
    load_id = State()


class TokenStorageState(StatesGroup):
    token = State()


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    token = get_user_by_telegram_id(message.from_user.id)
    if token:
        token = token[2]
        profile_details = get_profile_details(token)

        if profile_details:
            if profile_details:
                a = list(profile_details.keys())[0]
                await message.answer(
                    f"Wassup Mr. User! Here are your profile details:\n{profile_details}",
                    reply_markup=get_buttons_by_role(
                        profile_details[a]["user"]["user_type"]
                    ),
                )
            else:
                await message.answer(
                    "Welcome back! Please proceed with the registration process."
                )
                await RegistrationState.phonenumber.set()
        else:
            await message.answer(
                "Failed to fetch profile details. Please proceed with the registration process."
            )
            await RegistrationState.phonenumber.set()
    else:
        await message.answer(
            "Hi, let's create an account. Please enter your phone number:"
        )
        await RegistrationState.phonenumber.set()


@dp.message_handler(state=RegistrationState.phonenumber)
async def process_phonenumber(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phonenumber"] = message.text
    await message.answer(
        f"SMS activation code sent to the phone number: {message.text}."
        "Please enter the 4 digit code"
    )
    await RegistrationState.sms_code.set()


@dp.message_handler(state=RegistrationState.sms_code)
async def process_sms_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sms_code"] = message.text
    context = await state.get_data()
    response = verify_phonenumber(
        phonenumber=context.get("phonenumber"), code=message.text
    )
    if ("sms_code_status" in response.keys()) and (response["sms_code_status"]):
        await message.answer("Cool, now enter your fullname in this order: `John Doe`")
        await RegistrationState.fullname.set()
    else:
        await message.answer("SMS code is not valid")
        await RegistrationState.sms_code.set()


@dp.message_handler(state=RegistrationState.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.text.split(" ")) != 2:
            await message.answer("Please enter your fullname in this order: `John Doe`")
            await RegistrationState.fullname.set()
        data["fullname"] = message.text
    await message.answer("Please enter your password:")
    await RegistrationState.password.set()


@dp.message_handler(state=RegistrationState.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text
    await message.delete()
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Driver", callback_data="driver"),
        InlineKeyboardButton(text="Dispatcher", callback_data="dispatcher"),
        InlineKeyboardButton(text="Client", callback_data="client"),
    )
    await message.answer("Please select your role:", reply_markup=keyboard)
    await RegistrationState.role.set()


@dp.callback_query_handler(lambda c: c.data == "add_load", state="*")
async def add_load_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("Let's add a new load. Please provide the product name:")
    await LoadCreationState.product_name.set()


# Handler to gather product name
@dp.message_handler(state=LoadCreationState.product_name)
async def process_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_name"] = message.text
    await message.answer("Great! Now, please provide the product info:")
    await LoadCreationState.next()


# Handler to gather product info
@dp.message_handler(state=LoadCreationState.product_info)
async def process_product_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_info"] = message.text
    await message.answer("Please select the product type:")
    await LoadCreationState.next()


# Handler to gather product type
@dp.message_handler(state=LoadCreationState.product_type)
async def process_product_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_type"] = message.text
    await message.answer("Please provide the product count:")
    await LoadCreationState.next()


# Handler to gather product count
@dp.message_handler(state=LoadCreationState.product_count)
async def process_product_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_count"] = message.text
    await message.answer("Please provide the address:")
    await LoadCreationState.next()


# Handler to gather address
@dp.message_handler(state=LoadCreationState.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await message.answer("Finally, please provide the receiver phone number:")
    await LoadCreationState.next()


# Handler to gather receiver phone number
@dp.message_handler(state=LoadCreationState.receiver_phone_number)
async def process_receiver_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["receiver_phone_number"] = message.text
    await message.answer("Please provide the delivery date (e.g., YYYY-MM-DD):")
    await LoadCreationState.date_delivery.set()


# Handler to gather delivery date
@dp.message_handler(state=LoadCreationState.date_delivery)
async def process_delivery_date(message: types.Message, state: FSMContext):
    token = get_user_by_telegram_id(message.from_user.id)
    if token:
        token = token[2]
    async with state.proxy() as data:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", message.text):
            await message.answer(
                "Please enter the delivery date in the format YYYY-MM-DD."
            )
            await LoadCreationState.date_delivery.set()
            return
        data["date_delivery"] = message.text
        data["from_location"], data["to_location"] = [1], [1]
        response = client_add_load(data=data.as_dict(), token=token)
    await message.answer(f"Load details saved successfully!{response}")
    await state.finish()


@dp.callback_query_handler(
    lambda c: c.data in ["driver", "dispatcher", "client"],
    state=RegistrationState.role,
)
async def process_role_callback(query: types.CallbackQuery, state: FSMContext):
    role = query.data
    await state.update_data(role=role)
    data = await state.get_data()
    context_data = {
        "phonenumber": data["phonenumber"],
        "first_name": data["fullname"][0],
        "last_name": data["fullname"][-1],
        "telegram_id": query.from_user.id,
        "password": data["password"],
        "user_type": data["role"],
    }
    response = register_user(context_data)
    await TokenStorageState.token.set()
    await state.set_state(TokenStorageState.token)
    await state.update_data(token=response.get("access"))
    insert_user(telegram_id=query.from_user.id, token=response.get("access"))
    await state.finish()
    await bot.send_message(
        chat_id=query.message.chat.id, text=str(response), reply_markup=client_buttons
    )


@dp.callback_query_handler(lambda c: c.data == "request_dispatcher_to_driver")
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


@dp.callback_query_handler(lambda c: c.data.startswith("driver_get_load_"))
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

 
@dp.callback_query_handler(lambda c: c.data == "show_my_load")
async def client_show_my_load_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = get_client_personal_loads(token)
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )
 

@dp.callback_query_handler(lambda c: c.data == "show_load")
async def show_my_loads(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    else:
        pass
    response = get_my_loads(token=token)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=str(response),
        reply_markup=driver_my_loads_buttons(
            [(i["id"], i["client"]["user"]["id"]) for i in response["results"]]
        ),
    )


@dp.callback_query_handler(
    lambda c: c.data.startswith("dispatcher_driver_delivery_request_"),
    state=DeliveryRequestState.load_id,
)
async def dispatcher_request_to_driver_handler(
    query: types.CallbackQuery, state: FSMContext
):
    data = await state.get_data()
    print(data)
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    context = await state.get_data()
    load_id = query.data.split("_")[-1]
    driver_id = context["driver_id"]
    response = request_delivery(token=token, load_id=load_id, user_id=driver_id)
    await query.answer(str(response))


@dp.callback_query_handler(lambda c: c.data.startswith("driver_show_load_"))
async def proceed_driver_request_handler(query: types.CallbackQuery):
    load_id, client_id = query.data.split("_")[-2], query.data.split("_")[-1]
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = request_delivery(token=token, load_id=load_id, user_id=client_id)
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )


@dp.callback_query_handler(lambda c: c.data == "profile_view")
async def profile_view_callback(query: types.CallbackQuery, state: FSMContext):
    # Get token from FSM state
    token = get_user_by_telegram_id(query.from_user.id)
    # Request profile details
    profile_details = get_profile_details(token[2])

    # Process profile details, e.g., send to user
    if profile_details:
        # Process profile details, e.g., send to user
        profile_message = f"Profile details:\n{profile_details}"
        a = list(profile_details.keys())[0]
        await query.message.answer(
            profile_message,
            reply_markup=get_buttons_by_role(
                profile_details[a]["user"]["user_type"],
            ),
        )
    else:
        await query.message.answer("Failed to fetch profile details.")


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
    await bot.send_message(
        chat_id=query.message.chat.id, text=f"Requested fakely: {response}"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
