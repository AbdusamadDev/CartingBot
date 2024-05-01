from aiogram.dispatcher import FSMContext
from aiogram import types

from bot.states import *
from bot.buttons import *
from bot.database import *
from bot.client import *


async def login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phonenumber"] = message.text
    await message.answer(f"Please enter your password.")
    await LoginState.password.set()


async def share_number_for_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phonenumber"] = message.contact.phone_number
    await message.answer(f"Please enter your password.")
    await LoginState.password.set()


async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text
    await message.delete()
    context = await state.get_data()
    response = login_user(phonenumber=context.get("phonenumber"), password=message.text)
    if response["status_code"] == 401:
        await message.answer(
            "🚫 Authentication process failed! please try again by entering your phone number",
            reply_markup=contact_btn,
        )
        await LoginState.phonenumber.set()
    elif response["status_code"] == 200:
        # database will be updated with the resopnse access token
        # also the menu button will be sent to user based on the user_type
        new_token = response["message"]["access"]
        update_token(message.from_user.id, new_token=new_token)
        print(response)
        await message.answer(
            f"Welcome {message.from_user.username}, Pleased to see you again! What do we do today?",
            reply_markup=get_buttons_by_role(response["message"]["user_type"]),
        )
        await state.finish()
