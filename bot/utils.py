import requests
import base64

from bot.client import get_profile_details, user_exists_in_backend
from bot.database import get_user_by_telegram_id
from bot.buttons import contact_btn
from bot.states import *


async def prompt_registration(bot, telegram_id, exception):
    await bot.send_message(telegram_id, "👋")
    await exception(
        text="Carting Logistics Service botiga xush kelibsiz! Iltimos ro'yxatdan o'tish uchun telefon raqamingizni quyidagi ko'rinishda kiriting: +998 (xx) xxx-xx-xx [e.g +998941234567]",
        reply_markup=contact_btn,
    )
    await RegistrationState.phonenumber.set()
    return


async def authenticate(bot, telegram_id, profile_view=False):
    token = get_user_by_telegram_id(telegram_id)
    exception = lambda text, reply_markup=None: bot.send_message(
        telegram_id, text=text, reply_markup=reply_markup
    )
    if token:
        print("Token exists")
        token = token[2]
        profile_details = get_profile_details(token)
        if not user_exists_in_backend(telegram_id):
            await prompt_registration(bot, telegram_id, exception)
            return
        if profile_details["status_code"] == 401:
            print("Token is invalid")
            await exception(
                "Tashrif buyirganingizga ko'p vaqt o'tdi, iltimos login qilish uchun telefon raqamingizni kiriting!",
                reply_markup=contact_btn,
            )
            await LoginState.phonenumber.set()
            return
        elif profile_details["status_code"] == 200:
            print("Token is valid")
            if profile_view:
                print("Profile view mode is on, returning profile details")
                return profile_details["message"]
            else:
                print("Profile view mode is off, just returning token")
                return token
        print(profile_details)
    else:
        print("Token does not exist in database")
        if user_exists_in_backend(telegram_id):
            print("_______________________")
            print("User exists in backend")
            await exception("Iltimos login qilish uchun telefon raqamingizni kiriting!")
            await LoginState.phonenumber.set()
            return
        else:
            print("User does not exist in backend")
            await prompt_registration(bot, telegram_id, exception)
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


status = {
    "active": "🟩",
    "wait": "🟨",
    "cancel": "🟥",
    "process": "🟧",
    "wait_driver": "🟨",
    "confirmation_driver": "🟨",
    "unfinish_dispatcher": "⬜️",
    "unfinish_client": "⬜️",
    "finish": "🟦",
    "confirmation_dispatcher": "🟫",
    "wait_dispatcher": "🟨",
}

if __name__ == "__main__":
    print(is_valid("998940055565"))
