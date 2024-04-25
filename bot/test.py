import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from conf import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

class ButtonStates(StatesGroup):
    buttons = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 11)]
    keyboard_markup.add(*buttons)
    await message.answer("Click on a button:", reply_markup=keyboard_markup)
    await ButtonStates.buttons.set()

@dp.callback_query_handler(state=ButtonStates.buttons)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'clicked_buttons' not in data:
            data['clicked_buttons'] = []
        clicked_button = callback_query.data
        data['clicked_buttons'].append(clicked_button)
        clicked_buttons = data['clicked_buttons']
        
        keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
        remaining_buttons = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 11) if str(i) not in clicked_buttons]
        keyboard_markup.add(*remaining_buttons)
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=keyboard_markup)

@dp.message_handler(commands=['result'])
async def result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'clicked_buttons' in data:
            await message.answer("Clicked button IDs: " + ', '.join(data['clicked_buttons']))
        else:
            await message.answer("No buttons clicked yet.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
