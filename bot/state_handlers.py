from aiogram.dispatcher import FSMContext
from aiogram import types

from database import *
from buttons import *
from states import *
from client import *
from main import dp


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
async def add_load_handler(query: types.CallbackQuery):
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
        # create_load(data)
    await message.answer(str(data))
    await state.finish()


# Modify finish_district_selection to use the correct variable name
@dp.callback_query_handler(state=TokenStorageState.token)
async def finish_district_selection(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    async with state.proxy() as data:
        selected_districts = data.get("selected_districts", [])
        await query.message.answer("District selection completed successfully.")
        await query.message.answer(f"Selected Districts: {selected_districts}")
    await state.finish()
