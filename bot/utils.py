import requests
import base64

from bot.database import get_user_by_telegram_id
from bot.client import get_profile_details, user_exists_in_backend
from bot.buttons import contact_btn
from bot.states import LoginState


async def authenticate(bot, telegram_id, profile_view=False):
    token = get_user_by_telegram_id(telegram_id)
    exception = lambda text, reply_markup=None: bot.send_message(
        telegram_id, text=text, reply_markup=reply_markup
    )
    if token:
        token = token[2]
        profile_details = get_profile_details(token)
        if profile_details["status_code"] == 401:
            await exception(
                "Tashrif buyirganingizga ko'p vaqt o'tdi, iltimos login qilish uchun telefon raqamingizni kiriting!"
            )
            await LoginState.phonenumber.set()
            return
        elif profile_details["status_code"] == 200:
            if profile_view:
                return profile_details["message"]
            else:
                return token
        else:
            await bot.send_message(
                telegram_id,
                text="Tizimda kutilmagan xatolik yuz berdi, qayta urinib ko'ring!",
            )
            return
    else:
        if user_exists_in_backend(telegram_id):
            await exception("Iltimos login qilish uchun telefon raqamingizni kiriting!")
            await LoginState.phonenumber.set()
            return
        else:
            await bot.send_message(telegram_id, "👋")
            await exception(
                text="Carting Logistics Service botiga xush kelibsiz! Iltimos ro'yxatdan o'tish uchun telefon raqamingizni quyidagi ko'rinishda kiriting: +998 (xx) xxx-xx-xx [e.g +998941234567]",
                reply_markup=contact_btn,
            )
            return


def is_valid(input_string):
    # Check if input starts with '+'
    if not input_string.startswith("+"):
        return False

    # Check if length is exactly 13 characters
    if len(input_string) != 13:
        return False

    # Check if all characters after '+' are digits
    if not input_string[1:].isdigit():
        return False

    # If all conditions are met, return True
    return True


def get_districts(regions, selected_region):
    # Use next to find the first matching region and return its districts
    return next(
        (
            region["district"]
            for region in regions
            if region["pk"] == int(selected_region)
        ),
        [],
    )


def make_multiselect(markup, selected_district):
    # Simplify the logic for toggling the checkmark
    for item in markup["inline_keyboard"]:
        for inner_item in item:
            if inner_item["callback_data"] == f"district:{selected_district}":
                inner_item["text"] = (
                    "✅ " + inner_item["text"].lstrip("✅ ")
                    if "✅" not in inner_item["text"]
                    else inner_item["text"].replace("✅ ", "")
                )
    return markup


def get_selected_districts(markup):
    # Use a list comprehension for cleaner code
    return [
        int(inner_item["callback_data"].split(":")[-1])
        for item in markup["inline_keyboard"]
        for inner_item in item
        if "✅" in inner_item["text"]
    ]


def url_to_base64(image_url):
    try:
        response = requests.get(image_url)
        encoded_string = base64.b64encode(response.content)
        return encoded_string.decode("utf-8")
    except requests.exceptions.RequestException as e:
        return None


if __name__ == "__main__":
    print(is_valid("998940055565"))
