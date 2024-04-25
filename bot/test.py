from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from conf import TOKEN
from buttons import *

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Function to handle button clicks
@dp.callback_query_handler(lambda c: c.data.startswith("update_button"))
async def update_button_label(callback_query: types.CallbackQuery):
    # Extract the current button label
    current_label = callback_query.message.reply_markup.inline_keyboard[0][0].text
    # Update the label (for demonstration purposes, just adding ' Updated' to the existing label)
    index = 0
    updated_label = current_label + f" Updated {index} "
    # Edit the message with the updated button label
    n[0][0].text = updated_label
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Button with updated label",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=n),
    )
    index += 1


# Handler for the command to start the bot
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # Send a message with an inline keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=n)
    await message.answer("Click the button to update its label:", reply_markup=keyboard)


# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
