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
        query.message.chat.id,
        text="Zo'r, endi, iltimos, yukingizning rasmini yuboring!",
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
        "Yukingizni qanday nomlaysiz, unga nom bering..."
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
        "Yaxshi, iltimos, yukning qisqacha tavsifini bering."
    )  # Prompt user for more detailed load information
    await LoadCreationState.product_info.set()  # Move to the next state to collect more load information


async def process_product_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_info"] = message.text
    await message.answer(
        "Sizning yukingiz qanday yuk? Iltimos, quyidagini tanlang:",
        reply_markup=get_choices_button(),
    )
    await LoadCreationState.product_type.set()


async def process_choice_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["product_type"] = query.data.split(":")[-1]
    await bot.send_message(
        text="Endi yuk miqdorini kiriting, ishlov berish uchun faqat raqamlar kifoya qiladi...",
        chat_id=query.message.chat.id,
    )
    await LoadCreationState.product_count.set()


async def process_product_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit():
            await message.answer(
                "🚫 Yuqorida aytib o'tilganidek, iltimos, yuklaringizning faqat sonini ko'rsating."
            )
            await LoadCreationState.product_count.set()
            return
        data["product_count"] = int(message.text)
    await message.answer(
        "Sizning yukingiz qayerda joylashgan? Uning manzilini bera olasizmi?"
    )
    await LoadCreationState.address.set()


async def process_region_callback(query: types.CallbackQuery, state: FSMContext):
    selected_region = query.data.split(":")[-1]
    state_data = await state.get_data()
    districts = get_districts(
        regions=state_data["regions"], selected_region=selected_region
    )
    btn = get_district_selection_buttons(districts, state_data["end"])
    await query.message.edit_text(
        text="Endi, iltimos, yukingizni etkazib berish uchun marshrutni ko'rsating, haydovchiga ushbu yo'nalishda harakatlanishini osonlashtiradigan quyidagi viloyat va tumanlarni tanlang ...",
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
            f"Haydovchi viloyatning qaysi tumanlaridan o'tishi kerak?",
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
        "Deyarli tugattik. Iltimos, ushbu formatdagi yuk qabul qiluvchining telefon raqamini kiritish orqali jarayonni yakunlang: +998 (xx) xxx-xx-xx [e.g `+998991234567`]"
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
    await message.answer("Iltimos, viloyatlarni tanlang:", reply_markup=btn)
    await LoadCreationState.region.set()


# Handler to gather receiver phone number
async def process_receiver_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["receiver_phone_number"] = message.text
    await message.answer(
        "Iltimos, ushbu formatda etkazib berish sanasini ko'rsating: (e.g., YYYY-MM-DD):"
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
                "🚫 Bu sana yaroqsiz, iltimos, ushbu formatda yaroqli maʼlumotlarni kiriting: YYYY-MM-DD."
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
