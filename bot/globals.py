from bot.buttons import *
from bot.database import *
from bot.client import *
from bot.utils import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.states import *
from bot.conf import bot
import asyncio


async def profile_view_callback(query: types.CallbackQuery, state: FSMContext):
    telegram_id = query.from_user.id
    profile_details = await authenticate(bot, telegram_id, profile_view=True)
    await query.message.delete()
    a = list(profile_details.keys())[0]
    profile_details = profile_details[a]
    first_name = profile_details["first_name"] or "Ism kiritilmagan"
    last_name = profile_details["last_name"] or "Familiya kiritilmagan"
    phonenumber = profile_details["user"]["phonenumber"]
    user_type = profile_details["user"]["user_type"]
    profile_message = f"👤 Profilim:\n\n➡️ Ism: {first_name}\n➡️ Familiya: {last_name}\n📞 Telefon raqam: {phonenumber}\n👤 Profil turi: {user_type}"
    await query.message.answer(
        profile_message,
        reply_markup=get_buttons_by_role(
            profile_details["user"]["user_type"],
        ),
    )


async def reject_handler(query: types.CallbackQuery):
    await asyncio.sleep(1.5)
    await bot.send_message(query.from_user.id, text="Successfully rejected!")


async def get_notifications_handler(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    notifications = get_notifications(token)

    if notifications:
        message_text = "📬 <b>Notifications:</b>\n\n"
        for notification in notifications:
            load = notification["load"]
            load_name = load["product_name"]
            load_info = load["product_info"]
            load_count = load["product_count"]
            load_type = load["product_type"]
            load_status = load["status"]
            from_location = ", ".join(load["from_location"])
            to_location = ", ".join(load["to_location"])
            delivery_date = load["date_delivery"]

            message_text += f"📦 <b>Name:</b> {load_name}\n"
            message_text += f"ℹ️ <b>Info:</b> {load_info}\n"
            message_text += f"🔢 <b>Count:</b> {load_count}\n"
            message_text += f"📌 <b>Type:</b> {load_type}\n"
            message_text += f"📝 <b>Status:</b> {load_status}\n"
            message_text += f"📍 <b>From Location:</b> {from_location}\n"
            message_text += f"📍 <b>To Location:</b> {to_location}\n"
            message_text += f"📅 <b>Delivery Date:</b> {delivery_date}\n\n"

        await query.message.answer(text=message_text, parse_mode="HTML")
    else:
        await query.message.answer("No notifications available. 🤷‍♂️")


async def main_menu_callback_handler(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    profile_details = get_profile_details(token)
    print(profile_details)
    a = list(profile_details["message"].keys())[0]
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f"Xush kelibsz  {query.from_user.username}, iltimos, bajarmoqchi bo'lgan amalni tanlang!",
        reply_markup=get_buttons_by_role(a),
    )


async def confirm_handler(query: types.CallbackQuery):
    token = await authenticate(bot, query.from_user.id)
    user_type = query.data.split(":")[1]
    load_id = query.data.split(":")[-1]
    if user_type == "client":
        notification_id = query.data.split(":")[2]
        response = client_confirm_load_delivery(
            notification_id=notification_id, token=token
        )
        transaction_object = get_transaction(load_id)
        if transaction_object["status_code"] == 200:
            transaction_object = transaction_object["message"]
            if transaction_object["driver"] is not None:
                telegram_id = int(transaction_object["driver"]["user"]["telegram_id"])
                await bot.send_message(
                    telegram_id,
                    text=f"Siz yetkazib berish jarayonini boshlashingiz mumkin, mijoz endigina tasdiqladi va yukni yetkazib berishingizga ruxsat berdi, bajarganingizdan keyin ularga xabar bering va quyidagi `Yakunladim` tugmasini bosing.",
                    reply_markup=successfully_delivered_btn(load_id),
                )
        await bot.send_message(
            query.message.chat.id,
            text="Yukingizni olishga ruxsat berganingiz haqida haydovchi ogohlantirildi.",
        )
    elif user_type == "driver":
        pass
