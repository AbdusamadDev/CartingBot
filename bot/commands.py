from aiogram.dispatcher import FSMContext
from aiogram import types

from bot.buttons import get_buttons_by_role, contact_btn
from bot.states import LoginState, RegistrationState
from bot.utils import authenticate
from bot.conf import bot


async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    profile = await authenticate(bot, message.from_user.id, profile_view=True)
    if profile:
        user_type = list(profile.keys())[0]
        await message.answer(
            f"Salom hush kelibsiz {message.from_user.username}, Bugun nima qilamiz?",
            reply_markup=get_buttons_by_role(user_type),
        )
    else:
        await RegistrationState.phonenumber.set()
