from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.main import _


def main_menu_btn(user):
    keyboard = []
    orders = get_orders(user_id=user.id, status=1)

    if len(orders) > 0:
        keyboard.append([
            KeyboardButton(text=_("buyurtma_berish", locale=user.get_lang())),
            KeyboardButton(text=_("buyurtmalarim", locale=user.get_lang())),
        ])
    else:
        keyboard.append([
            KeyboardButton(text=_("buyurtma_berish", locale=user.get_lang())),
        ])

    keyboard.append(
        [
            KeyboardButton(text=_("hamyon", locale=user.get_lang())),
            # KeyboardButton(text=_("aloqa", locale=user.get_lang())),
            KeyboardButton(text=_("tarix", locale=user.get_lang())),
        ]
    )

    keyboard.append([
        KeyboardButton(text=_("sozlanmalar", locale=user.get_lang())),
    ])
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)

    return markup
