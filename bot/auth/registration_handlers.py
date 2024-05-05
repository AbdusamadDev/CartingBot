from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.database import *
from bot.buttons import *
from bot.states import *
from bot.client import *
from bot.utils import *
from bot.conf import bot


async def process_phonenumber(message: types.Message, state: FSMContext):
    if not is_valid(message.text):
        await message.answer("🚫 Iltimos yaroqli telefon raqam kiriting.")
        await RegistrationState.phonenumber.set()
        return
    async with state.proxy() as data:
        data["phonenumber"] = message.text
    await message.answer(
        f"4 ta raqamli faollashtirish kodi telefon raqamingizga yuborildi: {message.text}, faollashtirish kodini kiriting:"
    )
    await RegistrationState.sms_code.set()


async def share_number_for_registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phonenumber"] = message.contact.phone_number
    await message.answer(f"Parolingizni kiriting.")
    await RegistrationState.password.set()


async def process_sms_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sms_code"] = message.text
    context = await state.get_data()
    response = verify_phonenumber(
        phonenumber=context.get("phonenumber"), code=message.text
    )
    if ("sms_code_status" in response.keys()) and (response["sms_code_status"]):
        await message.answer("Yaxshi, endi kuchli parol kiriting!")
        await RegistrationState.password.set()
    else:
        await message.answer(
            "🚫 Activatsiya kodi noto'g'ri. Iltimos qayta urinib ko'ring"
        )
        await RegistrationState.sms_code.set()


async def handle_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    if (
        contact.user_id == message.from_user.id
    ):  # Ensuring the contact belongs to the sender
        phonenumber = contact.phone_number
        async with state.proxy() as data:
            data["phonenumber"] = phonenumber
        await message.answer(
            f"4 ta raqamli faollashtirish kodi telefon raqamingizga yuborildi: {message.text}, faollashtirish kodini kiriting: "
        )
        await RegistrationState.sms_code.set()
    else:
        await message.answer("Iltimos o'zingizni telefon raqamingizni kiriting.")


async def process_role_callback(query: types.CallbackQuery, state: FSMContext):
    role = query.data
    print(type(state))
    await state.update_data(role=role)
    data = await state.get_data()
    context_data = {
        "phonenumber": data["phonenumber"],
        "first_name": query.from_user.first_name,
        "last_name": query.from_user.last_name,
        "password": data["password"],
        "user_type": data["role"],
    }
    response = register_user(context_data, telegram_id=query.from_user.id)
    if response["status_code"] == 400:
        await bot.send_message(
            query.message.chat.id,
            "Ro'yxatdan o'tishda xatolik yuz berdi Qayta urining va telefon raqamingizni kiriting: +998 (xx) xxx-xx-xx [e.g `+998991234567`]",
        )
        await RegistrationState.phonenumber.set()
    else:
        await TokenStorageState.token.set()
        await state.set_state(TokenStorageState.token)
        token = response["message"]["access"]
        await state.update_data(token=token)
        await LoadDetailsState.loads.set()
        await state.set_data(LoadDetailsState.loads)
        insert_user(telegram_id=query.from_user.id, token=token)
        user_button = {
            "driver": driver_buttons,
            "client": get_clients_buttons(0),
            "dispatcher": dispatcher_buttons,
        }
        await state.finish()
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=f"🥳🥳🥳\Tabriklaymiz {context_data['first_name']} {context_data['last_name']}!\n\n Siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
            reply_markup=user_button[response["message"]["user_type"]],
        )


async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text
    await message.delete()
    await message.answer("Kim sifatida ro'xatdan o'tmoqchisiz?", reply_markup=keyboard)
    await RegistrationState.role.set()
