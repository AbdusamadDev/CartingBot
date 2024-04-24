from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor, Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from client import register_user, verify_phonenumber
from conf import TOKEN
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
auth_token = None


class RegistrationState(StatesGroup):
    fullname = State()
    phonenumber = State()
    sms_code = State()
    role = State()
    password = State()


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    await message.answer("Please provide your number:")
    await RegistrationState.phonenumber.set()


@dp.message_handler(state=RegistrationState.phonenumber)
async def process_phonenumber(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phonenumber"] = message.text
    await message.answer("SMS code sent. Please enter the code.")
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
        await message.answer("Enter fullname, and response: {}".format(response))
        await RegistrationState.fullname.set()
    else:
        await message.answer("SMS code is not valid")
        await RegistrationState.sms_code.set()


@dp.message_handler(state=RegistrationState.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fullname"] = message.text
    await message.answer("Please enter your password:")
    await RegistrationState.password.set()


@dp.message_handler(state=RegistrationState.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text
    await message.delete()

    # Inline keyboard markup with three buttons
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Driver", callback_data="driver"),
        InlineKeyboardButton(text="Dispatcher", callback_data="dispatcher"),
        InlineKeyboardButton(text="Client", callback_data="client"),
    )

    # Send the message with the inline keyboard
    await message.answer("Please select your role:", reply_markup=keyboard)
    await RegistrationState.role.set()


# Add a callback query handler to process the role selection
@dp.callback_query_handler(
    lambda c: c.data in ["driver", "dispatcher", "client"], state=RegistrationState.role
)
async def process_role_callback(query: types.CallbackQuery, state: FSMContext):
    role = query.data
    await state.update_data(role=role)

    # Now you have collected all the necessary information.
    # You can proceed with registering the user or performing any other necessary actions.
    data = await state.get_data()
    context_data = {
        "phonenumber": data["phonenumber"],
        "first_name": data["fullname"][0],
        "last_name": data["fullname"][-1],
        "password": data["password"],
        "user_type": data["role"],
    }
    print(context_data)
    response = register_user(context_data)
    await bot.send_message(chat_id=query.message.chat.id, text=str(response))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
