import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from conf import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class ButtonStates(StatesGroup):
    buttons = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await ButtonStates.buttons.set()
    await send_buttons(message)


async def send_buttons(message, clicked_buttons=None, state=None):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = [
        types.InlineKeyboardButton(str(i), callback_data=str(i))
        for i in range(1, 11)
    ]
    if clicked_buttons:
        clicked_buttons_list = clicked_buttons.split()
        buttons = [btn for btn in buttons if btn.text not in clicked_buttons_list]
    keyboard_markup.add(*buttons)
    await message.answer("Click on a button:", reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.isdigit())
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        clicked_button = callback_query.data
        if "clicked_buttons" not in data:
            data["clicked_buttons"] = ""
        data["clicked_buttons"] += f"{clicked_button} "
        await send_buttons(callback_query.message, data["clicked_buttons"])


@dp.message_handler(commands=["result"], state="*")
async def result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
    await message.answer(f"You clicked buttons: {data}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
