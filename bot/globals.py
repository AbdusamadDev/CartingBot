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
    # notificationID, status, action
    print(111111111111111111111111, query.data)
    token = get_user_by_telegram_id(query.from_user.id)
    if token:
        token = token[2]
    user_type = query.data.split(":")[1]
    transaction_id = query.data.split(":")[-1]
    if user_type == "client":
        notification_id = query.data.split(":")[2]
        print(notification_id)
        response = client_confirm_load_delivery(
            notification_id=notification_id, token=token
        )
        transaction_object = get_transaction(transaction_id)
        print(transaction_object)
        if transaction_object["status_code"] == 200:
            transaction_object = transaction_object["message"]
            print(int(transaction_object["driver"]["user"]["telegram_id"]))
            if transaction_object["driver"] is not None:
                print("I AM SENDING NOTIFICATION TO DRIVER")
                telegram_id = int(transaction_object["driver"]["user"]["telegram_id"])
                await bot.send_message(
                    telegram_id,
                    text=f"You can start delivery process, client has just confirmed and let you delivery the load, let them know when you are done and click finished button below",
                    reply_markup=successfully_delivered_btn(transaction_id),
                )
        await bot.send_message(query.message.chat.id, text=f"Salom bacha {response}")
    elif user_type == "driver":
        pass


{
    "message": {
        "uuid": "a8f1068f-a24c-4266-99d6-2e1007b6d213",
        "load": {
            "receiver_phone_number": "+998999999999",
            "product_count": 33.0,
            "date_delivery": "2000-01-01T00:23:00+05:00",
            "product_name": "asdfasdf",
            "product_info": "as",
            "product_type": "m",
            "from_location": ["a"],
            "to_location": ["aaaaaa"],
            "address": "asdfasfasdfsda",
            "status": "wait",
            "product_image": "http://localhost:8000/media/load_images/3ddf8ed4-9540-493a-aaef-f132be710951.jpg",
            "id": 1,
            "client": {
                "first_name": None,
                "last_name": None,
                "obj_status": "available",
                "user": {
                    "phonenumber": "+998940022256",
                    "user_type": "client",
                    "first_name": None,
                    "last_name": None,
                    "telegram_id": 2003049919,
                    "id": 2,
                },
            },
        },
        "created_at": "2024-05-02T07:59:07+05:00",
        "updated_at": "2024-05-02T07:59:07+05:00",
        "obj_status": "available",
        "status": "wait_driver",
        "review": 0,
        "driver": {
            "user": {
                "phonenumber": "+998941234563",
                "first_name": None,
                "last_name": None,
            }
        },
        "dispatcher": None,
    },
    "status_code": 200,
}
