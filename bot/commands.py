from aiogram.dispatcher import FSMContext
from aiogram import types
import logging

from bot.states import LoginState, RegistrationState
from bot.database import get_user_by_telegram_id
from bot.buttons import get_buttons_by_role
from bot.client import get_profile_details


async def start_handler(message: types.Message, state: FSMContext):
    user = get_user_by_telegram_id(message.from_user.id)
    if user:
        logging.info(f"The user details from database: {user}")
        profile = get_profile_details(user[2])
        # User exists in database
        if profile["status_code"] == 401:
            # User in database but doesnt have valid token to perform actions
            await message.answer(
                "🚫 Sorry, unable to recognize you, please enter you phone number to login."
            )
            logging.info("SETTING phonenumber state")
            await LoginState.phonenumber.set()
        else:
            # User has valid token and authenticated
            print("Profile: ", profile)
            user_type = list(profile["message"].keys())[0]
            await message.answer(
                f"Welcome back {message.from_user.username}, What do we do today?",
                reply_markup=get_buttons_by_role(user_type),
            )
    else:
        # Fresh registration, user is not in database
        await message.answer(
            "Welcom to Carting Logistics Service bot! Please start typing your phone number in following format: +998 (xx) xxx-xx-xx [e.g +998941234567]"
        )
        await RegistrationState.phonenumber.set()
