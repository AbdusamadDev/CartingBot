from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor, Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

from conf import TOKEN
from database import *
from buttons import *
from client import *
from states import *


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
auth_token = None
create_table()


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    token = get_user_by_telegram_id(message.from_user.id)
    if token:
        token = token[2]
        print(token)
        # If token exists, request profile details
        profile_details = get_profile_details(token)

        if profile_details:
            # If status code is 200, return profile details
            if profile_details:
                print("Profile details: ", profile_details)
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


dp.register_callback_query_handler(
    process_role_callback,
    lambda c: c.data in ["driver", "dispatcher", "client"],
    state=RegistrationState.role,
)
dp.register_callback_query_handler(
    profile_view_callback, lambda c: c.data == "profile_view"
)
dp.register_callback_query_handler(
    load_details_handler, lambda c: c.data == "load_details", state="*"
)

dp.register_callback_query_handler(
    process_district_selection, lambda c: c.data.startswith("district_"), state="*"
)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from state_handlers import *
    from query_handlers import *

    executor.start_polling(dp, skip_updates=True)
