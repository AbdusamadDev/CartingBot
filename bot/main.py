from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor, Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
import logging
import asyncio
import re

from conf import TOKEN
from database import *
from buttons import *
from states import *
from client import *
from utils import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
auth_token = None
create_table()


# ###########################################################################
# ###########################################################################
# ###########################################################################
# Start command
@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    token = get_user_by_telegram_id(message.from_user.id)
    if token:
        token = token[2]
        profile_details = get_profile_details(token)
        if profile_details:
            if "detail" in profile_details:
                await message.answer(
                    "🚫 Authentication process failed!",
                )
                await asyncio.sleep(0.6)
                await message.delete()
                await message.answer(
                    "Let's process a quick registration, please enter your phone number in format: +998 (xx) xxx-xx-xx [e.g `+998991234567`]"
                )
                await RegistrationState.phonenumber.set()
            else:
                a = list(profile_details.keys())[0]
                await message.answer(
                    f"Welcome {message.from_user.username}, Pleased to see you again! What do we do today?",
                    reply_markup=get_buttons_by_role(
                        profile_details[a]["user"]["user_type"]
                    ),
                )
        else:
            await message.answer(
                "🚫 Oops, Unable to recognize you, please Enter your phonenumber for registration."
            )
            await RegistrationState.phonenumber.set()
    else:
        btn = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(
                        text="Share my phone number", request_contact=True
                    )
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await message.answer("👋")
        await message.answer(
            "Welcome to the Carting Logistics Service bot! \n\nLet's register your details for the service. Please enter your phone number in format:  +998 (xx) xxx-xx-xx [e.g `+998991234567`]",
            reply_markup=btn,
        )
        await RegistrationState.phonenumber.set()


# ###########################################################################
# ###########################################################################
# ###########################################################################
# Registration


@dp.message_handler(state=RegistrationState.phonenumber)
async def process_phonenumber(message: types.Message, state: FSMContext):
    if not is_valid(message.text):
        await message.answer(
            "🚫 Sorry, this didn't work, try entering valid phone number."
        )
        await RegistrationState.phonenumber.set()
        return
    async with state.proxy() as data:
        data["phonenumber"] = message.text
    await message.answer(
        f"4-digit activation code was immediately sent to your phone number: {message.text}, please enter this code"
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
        await message.answer(
            "Now please enter your fullname in this format: `John Doe`"
        )
        await RegistrationState.fullname.set()
    else:
        await message.answer(
            " Activation code is invalid. Try again by clicking /start"
        )
        await state.finish()


@dp.message_handler(state=RegistrationState.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.text.split(" ")) != 2:
            await message.answer(
                "🚫 Please enter valid fullname in this format: `John Doe`"
            )
            await RegistrationState.fullname.set()
            return
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
        InlineKeyboardButton(text="🚛 Driver", callback_data="driver"),
        InlineKeyboardButton(text="👨‍🔧 Dispatcher", callback_data="dispatcher"),
        InlineKeyboardButton(text="👤Client", callback_data="client"),
    )
    await message.answer("Who do you want to register as?", reply_markup=keyboard)
    await RegistrationState.role.set()


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
        "first_name": data["fullname"].split(" ")[0],
        "last_name": data["fullname"].split(" ")[-1],
        "telegram_id": query.from_user.id,
        "password": data["password"],
        "user_type": data["role"],
    }
    response = register_user(context_data)
    if "detail" in response.keys():
        await bot.send_message(
            "Sorry, Unable to recognize you, please enter your phone number for quick registration in this format: +998 (xx) xxx-xx-xx [e.g `+998991234567`]"
        )
        await RegistrationState.phonenumber.set()
    await TokenStorageState.token.set()
    await state.set_state(TokenStorageState.token)
    await state.update_data(token=response.get("access"))
    insert_user(telegram_id=query.from_user.id, token=response.get("access"))
    user_button = {
        "driver": driver_buttons,
        "client": client_buttons,
        "dispatcher": dispatcher_buttons,
    }
    await state.finish()
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"🥳🥳🥳\nCongratulations {context_data['first_name']} {context_data['last_name']}!\n\n Now you are shiny part of Carting Logistics Service!\n\Please select the action you want to perform.",
        reply_markup=user_button[response["user_type"]],
    )


# ###########################################################################
# ###########################################################################
# ###########################################################################
# Load creation


@dp.callback_query_handler(lambda query: query.data == "add_load")
async def process_add_load_callback(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        query.message.chat.id, text="Cool now, Please send your load's picture please!"
    )
    await LoadCreationState.image.set()


@dp.message_handler(state=LoadCreationState.image, content_types=["photo"])
async def add_load_handler(message: types.Message, state: FSMContext):
    """
    Handles the addition of a load image by the user. It saves the image URL to the state
    and prompts the user to provide the name of the load.

    Parameters:
    - message: types.Message
        The message from the user, expected to contain a photo.
    - state: FSMContext
        The finite state machine context to store data across different handler calls.

    The function extracts the URL of the last photo sent by the user, saves it in the state,
    and asks the user to provide the name of the load next.
    """
    photo_url = await message.photo[
        -1
    ].get_url()  # Await the coroutine to get the actual URL
    async with state.proxy() as data:
        data["image"] = photo_url  # Save the photo URL in the state
    await message.answer(
        "How do you title your load as, please give a name for it..."
    )  # Prompt user for the load name
    await LoadCreationState.product_name.set()  # Move to the next state to collect load name


@dp.message_handler(state=LoadCreationState.product_name)
async def process_product_name(message: types.Message, state: FSMContext):
    """
    Processes the load name provided by the user. It saves the load name to the state
    and prompts the user to provide additional information about the load.

    Parameters:
    - message: types.Message
        The message from the user, expected to contain the name of the load.
    - state: FSMContext
        The finite state machine context to store data across different handler calls.

    The function saves the provided load name in the state and asks the user to provide
    more detailed information about the load.
    """
    async with state.proxy() as data:
        data["product_name"] = message.text  # Save the provided load name in the state
    await message.answer(
        "Okay, please provide a brief description of the load."
    )  # Prompt user for more detailed load information
    await LoadCreationState.next()  # Move to the next state to collect more load information


@dp.message_handler(state=LoadCreationState.product_info)
async def process_product_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_info"] = message.text
    await message.answer(
        "What kind of load is your load? Please select following",
        reply_markup=get_choices_button(),
    )
    await LoadCreationState.next()


@dp.callback_query_handler(text_contains="choice")
async def process_choice_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["product_type"] = query.data.split(":")[-1]
    await bot.send_message(
        text="Now please enter the amount of your load, just digits are enough to process...",
        chat_id=query.message.chat.id,
    )
    await LoadCreationState.next()


@dp.message_handler(state=LoadCreationState.product_count)
async def process_product_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit():
            await message.answer(
                "🚫 As it is mentioned, please provide only number of your load(s)."
            )
            await LoadCreationState.product_count.set()
            return
        data["product_count"] = int(message.text)
    await message.answer("Where is your load located? Can you provide its location?")
    await LoadCreationState.address.set()


@dp.callback_query_handler(state=LoadCreationState.region, text_contains="region:")
async def process_region_callback(query: types.CallbackQuery, state: FSMContext):
    selected_region = query.data.split(":")[-1]
    state_data = await state.get_data()
    districts = get_districts(
        regions=state_data["regions"], selected_region=selected_region
    )
    btn = get_district_selection_buttons(districts, state_data["end"])
    await query.message.edit_text(
        text="Now, please provide route for your load to be delivered, choose following regions and districts which helps driver to drive these direction much more easier...",
        reply_markup=btn,
    )
    await LoadCreationState.next()


@dp.callback_query_handler(state=LoadCreationState.district, text_contains="district")
async def process_district_callback(query: types.CallbackQuery, state: FSMContext):
    if query.data == "district_next":
        from_location = get_selected_districts(query.message.reply_markup)
        await state.update_data(from_location=from_location, end=True)
        token = get_user_by_telegram_id(query.from_user.id)
        regions = fetch_districts_details(token[2])
        btn = regions_btn(regions)
        with state.proxy as data:
            region = data["region"]
            await query.message.edit_text(
                f"Which districts of {region} should driver drive through?",
                reply_markup=btn,
            )
        await LoadCreationState.region.set()
    else:
        selected_district = query.data.split(":")[-1]
        btn = make_multiselect(query.message.reply_markup, selected_district)
        await query.message.edit_reply_markup(reply_markup=btn)


@dp.callback_query_handler(
    state=LoadCreationState.district, text="next_to_receiver_phone_number"
)
async def process_address_callback(query: types.CallbackQuery, state: FSMContext):
    to_location = get_selected_districts(query.message.reply_markup)
    await state.update_data(to_location=to_location)
    await query.message.answer(
        "Almost there, please finalize process by entering a phone number of load reciever in this format: +998 (xx) xxx-xx-xx [e.g `+998991234567`]"
    )
    await LoadCreationState.receiver_phone_number.set()


# Handler to gather address
@dp.message_handler(state=LoadCreationState.address)
async def process_address(message: types.Message, state: FSMContext):
    token = get_user_by_telegram_id(message.from_user.id)
    regions = fetch_districts_details(token[2])
    async with state.proxy() as data:
        data["address"] = message.text
        data["regions"] = regions
        data["end"] = False
    btn = regions_btn(regions)
    await message.answer("Please select region:", reply_markup=btn)
    await LoadCreationState.region.set()


# Handler to gather receiver phone number
@dp.message_handler(state=LoadCreationState.receiver_phone_number)
async def process_receiver_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["receiver_phone_number"] = message.text
    await message.answer(
        "Please provide the delivery date in this format: (e.g., YYYY-MM-DD):"
    )
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
                "🚫 Oops! This is not valid date, please enter valid data in this format: YYYY-MM-DD."
            )
            await LoadCreationState.date_delivery.set()
            return
        data["date_delivery"] = message.text
        image_blob = url_to_blob(data["image"])
        data.pop("image")
        response = client_add_load(
            data=data.as_dict(), token=token, image_blob=image_blob
        )
    await message.answer(
        f"Cool, your load {data['name']} was successfully added!",
        reply_markup=take_me_back_markup,
    )
    await state.finish()


# ###########################################################################
# ###########################################################################
# ###########################################################################
# Query Handlers


@dp.callback_query_handler(text_contains="main_menu")
async def main_menu_callback_handler(query: types.CallbackQuery):
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"Welcome back  {query.from_user.username}, please an action you want to perform!",
        reply_markup=get_buttons_by_role(),
    )


@dp.callback_query_handler(lambda c: c.data == "notifications")
async def get_notifications_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    notifications = get_notifications(token)
    await bot.send_message(query.message.chat.id, text=str(notifications))


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
        reply_markup=get_loads_button(
            indices=[(i["id"], i["product_name"]) for i in loads["results"]]
        ),
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
            [
                (i["product_name"], i["id"], i["client"]["user"]["id"])
                for i in response["results"]
            ]
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
    token = get_user_by_telegram_id(query.from_user.id)
    profile_details = get_profile_details(token[2])
    if profile_details:
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
