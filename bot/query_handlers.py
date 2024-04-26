from aiogram.dispatcher import FSMContext
from aiogram import types

from database import *
from buttons import *
from states import *
from client import *
from main import bot
from main import dp


async def process_role_callback(query: types.CallbackQuery, state: FSMContext):
    role = query.data
    await state.update_data(role=role)
    data = await state.get_data()
    context_data = {
        "phonenumber": data["phonenumber"],
        "first_name": data["fullname"][0],
        "last_name": data["fullname"][-1],
        "telegram_id": query.from_user.id,
        "password": data["password"],
        "user_type": data["role"],
    }
    print(context_data)
    response = register_user(context_data)
    print("_________" * 5)
    print(response.get("access"))
    await TokenStorageState.token.set()
    await state.set_state(TokenStorageState.token)
    await state.update_data(token=response.get("access"))
    insert_user(telegram_id=query.from_user.id, token=response.get("access"))
    await state.finish()
    await bot.send_message(
        chat_id=query.message.chat.id, text=str(response), reply_markup=client_buttons
    )


async def profile_view_callback(query: types.CallbackQuery, state: FSMContext):
    # Get token from FSM state
    print("Token obtained from FSM state")
    token = get_user_by_telegram_id(query.from_user.id)
    print("Get profile request")
    # Request profile details
    profile_details = get_profile_details(token[2])
    print("Profile details: ", profile_details)

    # Process profile details, e.g., send to user
    if profile_details:
        # Process profile details, e.g., send to user
        profile_message = f"Profile details:\n{profile_details}"
        a = list(profile_details.keys())[0]
        await query.message.answer(
            profile_message,
            reply_markup=get_buttons_by_role(
                profile_details[a]["user"]["user_type"],
            ),
        )
    else:
        await query.message.answer("Failed to fetch profile details.")


async def load_details_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer(
        "You have selected to see the load details.\nPlease select the district(s):",
        reply_markup=get_district_selection_buttons(),
    )
    await TokenStorageState.token.set()


# Handler to gather district selection
async def process_district_selection(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    district = query.data.split("_")[1]
    async with state.proxy() as data:
        if "selected_districts" not in data:
            data["selected_districts"] = []
        if district not in data["selected_districts"]:
            data["selected_districts"].append(district)
    await query.message.answer(f"District {district} selected ✅")
    await TokenStorageState.next()
