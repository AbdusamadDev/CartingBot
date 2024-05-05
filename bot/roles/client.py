from aiogram.dispatcher import FSMContext
from bot.states import *
from bot.conf import bot
from aiogram import types
from bot.buttons import *
from bot.client import *
from bot.database import *
from bot.utils import *
import re


async def process_add_load_callback(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        query.message.chat.id, text="Cool now, Please send your load's picture please!"
    )
    await LoadCreationState.image.set()


async def process_image_handler(message: types.Message, state: FSMContext):
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
    await LoadCreationState.product_info.set()  # Move to the next state to collect more load information


async def process_product_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_info"] = message.text
    await message.answer(
        "What kind of load is your load? Please select following",
        reply_markup=get_choices_button(),
    )
    await LoadCreationState.product_type.set()


async def process_choice_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["product_type"] = query.data.split(":")[-1]
    await bot.send_message(
        text="Now please enter the amount of your load, just digits are enough to process...",
        chat_id=query.message.chat.id,
    )
    await LoadCreationState.product_count.set()


async def process_product_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit():
            await message.answer(
                "🚫 As it is mentioned, please provide only number of your load(s)."
            )
            await LoadCreationState.product_count.set()
            return
        data["product_count"] = int(message.text)
    await message.answer("Where is your load located? Can you provide its address?")
    await LoadCreationState.address.set()


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


async def process_district_callback(query: types.CallbackQuery, state: FSMContext):
    if query.data == "district_next":
        from_location = get_selected_districts(query.message.reply_markup)
        await state.update_data(from_location=from_location, end=True)
        token = get_user_by_telegram_id(query.from_user.id)
        regions = fetch_districts_details(token[2])
        btn = regions_btn(regions)
        await query.message.edit_text(
            f"Which districts of the region should driver drive through?",
            reply_markup=btn,
        )
        await LoadCreationState.region.set()
    else:
        selected_district = query.data.split(":")[-1]
        btn = make_multiselect(query.message.reply_markup, selected_district)
        await query.message.edit_reply_markup(reply_markup=btn)


async def process_address_callback(query: types.CallbackQuery, state: FSMContext):
    to_location = get_selected_districts(query.message.reply_markup)
    await state.update_data(to_location=to_location)
    await query.message.answer(
        "Almost there, please finalize process by entering a phone number of load reciever in this format: +998 (xx) xxx-xx-xx [e.g `+998991234567`]"
    )
    await LoadCreationState.receiver_phone_number.set()


# Handler to gather address
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
async def process_receiver_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["receiver_phone_number"] = message.text
    await message.answer(
        "Please provide the delivery date in this format: (e.g., YYYY-MM-DD):"
    )
    await LoadCreationState.date_delivery.set()


# Handler to gather delivery date
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
        image_blob = url_to_base64(data["image"])
        data.pop("image")
        response = client_add_load(
            data=data.as_dict(), token=token, image_blob=image_blob
        )
    await message.answer(
        # f"Cool, your load {data['product_name']} was successfully added!",
        str(response),
        reply_markup=take_me_back_markup,
    )
    await state.finish()


async def client_show_my_load_handler(query: types.CallbackQuery, state: FSMContext):
    print(query.data)
    index = int(query.data.split(":")[-1])
    token = await authenticate(bot, query.from_user.id)
    response = get_client_personal_loads(token)
    if "Qabul qiluvchining telefon raqami" in query.message.text:
        await query.message.delete()
    if response["status_code"] == 200:
        response = response["message"]
        print(index)
        detail = response[index]
        status = {"active": "🟩", "wait": "🟦", "cancel": "🟥", "process": "🟨"}
        message_list = [
            f"\n\n ☎️ Qabul qiluvchining telefon raqami: {detail['receiver_phone_number']}",
            f"\n\n 🔢 Miqdori: {detail['product_count']}",
            f"\n\n 🏷 Nomi: {detail['product_name']}",
            f"\n\n 📐 Turi: {detail['product_type']}",
            f"\n\n 🖼 Rasm: {detail['product_image']}",
            f"\n\n 📍 Manzili: {detail['address']}",
            f"\n\n {status[detail['status']]} Holati: {detail['status']}",
            f"\n\n 📅 Qabul qilish sanasi: {detail['date_delivery']}",
            "Yukning yo`nalishi: "
            + "".join([f"📍 {i} --> " for i in detail["from_location"]])[:-4],
        ]
    async with state.proxy() as data:
        page = int(data.get("page", 0))
        max_length = int(data.get("max_length", len(response) - 1))
        if page > max_length:
            page = 0
        data["page"] = page + 1
        btns = [
            loads_button(page, "▶️ Keyingisi: " + response[page]["product_name"]),
            InlineKeyboardButton(text="Asosiy menyu", callback_data="main_menu"),
        ]
        btn = InlineKeyboardMarkup(row_width=1)
        btn.add(*btns)
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Batafsil: \n\n" + "".join(message_list),
            reply_markup=btn,
        )


[
    {
        "receiver_phone_number": "+998991234567",
        "product_count": 222.0,
        "date_delivery": "2024-01-01T00:23:00+05:00",
        "product_name": "qweqweqw",
        "product_info": "asdasdasd",
        "product_type": "m",
        "from_location": ["Pop"],
        "to_location": ["Angren"],
        "address": "asdasdasd",
        "status": "active",
        "product_image": "http://new-api.carting.uz/media/load_images/188d7fd3-dfd2-4577-bb80-fab0920959a0.jpg",
        "id": 144,
        "client": {
            "first_name": None,
            "last_name": None,
            "obj_status": "available",
            "user": {
                "phonenumber": "+998996685214",
                "user_type": "client",
                "first_name": None,
                "last_name": None,
                "id": 263,
            },
        },
    }
]


async def client_FINISH_processes(query: types.CallbackQuery):
    transaction_uuid = query.data.split("splitting_part")[-1]
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    response = client_FINISH_all_processes_request(
        transaction_id=transaction_uuid,
        token=token,
        action="finish_client",
        status="yes",
    )
    await bot.send_message(query.from_user.id, text=str(response))
