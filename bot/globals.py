from bot.buttons import *
from bot.database import *
from bot.client import *
from bot.utils import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.states import *
from bot.conf import bot


async def profile_view_callback(query: types.CallbackQuery, state: FSMContext):
    token = get_user_by_telegram_id(query.from_user.id)
    profile_details = get_profile_details(token[2])
    if profile_details:
        profile_message = f"Profile details:\n{profile_details}"
        a = list(profile_details["message"].keys())[0]
        await query.message.answer(
            profile_message,
            reply_markup=get_buttons_by_role(
                profile_details["message"][a]["user"]["user_type"],
            ),
        )
    else:
        await query.message.answer("Failed to fetch profile details.")


async def get_notifications_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    notifications = get_notifications(token)
    await bot.send_message(query.message.chat.id, text=str(notifications))


async def main_menu_callback_handler(query: types.CallbackQuery):
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        print(token)
        token = token[2]
    profile_details = get_profile_details(token)
    print(profile_details)
    a = list(profile_details["message"].keys())[0]
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"Welcome back  {query.from_user.username}, please select an action you want to perform!",
        reply_markup=get_buttons_by_role(a),
    )


async def confirm_handler(query: types.CallbackQuery):
    print(query.data)
    # confirm_request:client:1
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    user_type = query.data.split(":")[1]
    print("QQQQQQQQQQQQQQQQQQQQQ")
    if user_type == "client":
        notification_id = query.data.split(":")[-1]
        print(notification_id)
        print("NNNNNNNNNNNNNNNNNN")
        response = client_confirm_load_delivery(
            notification_id=notification_id, token=token
        )
        await bot.send_message(query.message.chat.id, text=f"Salom bacha {response}")
    elif user_type == "driver":
        pass
