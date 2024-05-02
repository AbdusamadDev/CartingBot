from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
import requests

from bot.conf import DOMAIN


notifications_button = InlineKeyboardButton(
    text="🔔 Show my notifications",
    callback_data="notifications",
)
driver_all_loads_btn = InlineKeyboardButton(
    text="Show all loads", callback_data="show_all_driver_loads"
)

client_buttons = InlineKeyboardMarkup(row_width=2)
client_btn = [
    notifications_button,
    InlineKeyboardButton(text="📦 My loads", callback_data="show_my_load"),
    InlineKeyboardButton(text="➕ Add load", callback_data="add_load"),
    InlineKeyboardButton(text="👤 My profile", callback_data="profile_view"),
]
client_buttons.add(*client_btn)


driver_buttons = InlineKeyboardMarkup()
driver_btn = [
    notifications_button,
    InlineKeyboardButton(text="📦 My loads", callback_data="show_load"),
    InlineKeyboardButton(text="👤 My profile", callback_data="profile_view"),
    driver_all_loads_btn,
]
driver_buttons.add(*driver_btn)

dispatcher_buttons = InlineKeyboardMarkup()
dispatcher_btn = [
    notifications_button,
    InlineKeyboardButton(
        text="📦📦 All loads", callback_data="dispatcher_show_all_loads"
    ),
    InlineKeyboardButton(
        text="🚚 Request delivery from drivers",
        callback_data="request_dispatcher_to_driver",
    ),
    InlineKeyboardButton(
        text="👥 Available Drivers", callback_data="dispatcher_show_drivers"
    ),
    InlineKeyboardButton(text="📦 My Loads", callback_data="dispatcher_get_my_loads"),
    InlineKeyboardButton(text="👤 My profile", callback_data="profile_view"),
]
dispatcher_buttons.add(*dispatcher_btn)


def get_loads_button(indices):
    keyboard = InlineKeyboardMarkup()
    for load_id, name in indices:
        keyboard.add(
            InlineKeyboardButton(
                text=f"📦 {name}",
                callback_data=f"dispatcher_driver_delivery_request_{load_id}",
            )
        )
    return keyboard


def get_loads_for_driver(indices):
    markup = InlineKeyboardMarkup(row_width=1)
    print(indices)
    print("++++++++++++++")
    for load_id, name in indices:
        markup.add(
            InlineKeyboardButton(
                text=f"📦 {name}",
                callback_data=f"driver_request_to_client:{load_id}",
            )
        )
    return markup


def successfully_delivered_btn(transaction_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Successfully delivered the load",
            callback_data=f"driver_successfully_delivered:{transaction_id}",
        )
    )
    return markup


contact_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Share my phone number", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def driver_my_loads_buttons(indices):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for load_name, load_id, client_id in indices:
        keyboard.add(
            InlineKeyboardButton(
                text=f"✅ {load_name}",
                callback_data=f"driver_show_load_{load_id}_{client_id}",
            )
        )
    return keyboard


def get_driver_buttons(indices):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for driver_id, fullname in indices:
        keyboard.add(
            InlineKeyboardButton(
                text=f"👤 {fullname}",
                callback_data=f"driver_get_loads_profile_view:{driver_id}",
            )
        )
    return keyboard


def get_one_driver_button(driver_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=f"Request to this driver",
            callback_data=f"driver_get_load_{driver_id}",
        )
    )
    return keyboard


def get_buttons_by_role(role):
    user_button = {
        "driver": driver_buttons,
        "client": client_buttons,
        "dispatcher": dispatcher_buttons,
    }
    return user_button[role]


def regions_btn(regions: list):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        *[
            InlineKeyboardButton(
                text=f'📍 {region["name"]}',
                callback_data=f"region:{region['pk']}",
            )
            for region in regions
        ]
    )
    return keyboard


# Define the function to generate district selection buttons
def get_district_selection_buttons(districts, end=False):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        *[
            InlineKeyboardButton(
                text=f'📍 {district["name"]}',
                callback_data=f"district:{district['pk']}",
            )
            for district in districts
        ],
    )
    if end:
        next_btn = InlineKeyboardButton(
            text="Next ⏩",
            callback_data="next_to_receiver_phone_number",
        )
    else:
        next_btn = InlineKeyboardButton(
            text="Next ⏩",
            callback_data="district_next",
        )
    keyboard.row(next_btn)
    return keyboard


def get_choices_button():
    request = requests.get(DOMAIN + "/clients/load-choices/")
    response = request.json()
    print(response)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        *[
            InlineKeyboardButton(
                text=f"✔️ {choice[-1]}", callback_data=f"choice:{choice[0]}"
            )
            for choice in response["choices"]
        ]
    )
    return keyboard


take_me_back_markup = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Main menu", callback_data="main_menu")
)
