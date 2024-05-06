from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
import requests

from bot.conf import DOMAIN


notifications_button = InlineKeyboardButton(
    text="🔔 Mening eslatmalarim",
    callback_data="notifications",
)
driver_all_loads_btn = InlineKeyboardButton(
    text="Barcha yuklarni ko'rish", callback_data="show_all_driver_loads"
)

loads_button = lambda index, text: InlineKeyboardButton(
    text=text, callback_data=f"show_my_load:{index}"
)


def load_creation_retry_btn():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Qayta urinish", callback_data="retry_add_load")
    )
    return markup


def get_clients_buttons(index):
    client_buttons = InlineKeyboardMarkup(row_width=2)
    client_btn = [
        notifications_button,
        loads_button(index, "📦 Mening yuklarim"),
        InlineKeyboardButton(text="➕ Yuk qo'shish", callback_data="add_load"),
        InlineKeyboardButton(text="👤 Mening Profilim", callback_data="profile_view"),
    ]
    client_buttons.add(*client_btn)
    return client_buttons


driver_buttons = InlineKeyboardMarkup()
driver_btn = [
    notifications_button,
    InlineKeyboardButton(text="📦 Mening yuklarim", callback_data="show_load"),
    InlineKeyboardButton(text="👤 Mening Profilim", callback_data="profile_view"),
    driver_all_loads_btn,
]
driver_buttons.add(*driver_btn)

keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(
    InlineKeyboardButton(text="🚛 Haydovchi", callback_data="driver"),
    # InlineKeyboardButton(text="👨‍🔧 Dispatcher", callback_data="dispatcher"),
    InlineKeyboardButton(text="👤 Foydalanuvchi", callback_data="client"),
)

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
    InlineKeyboardButton(
        text="📦 Mening yuklasrim", callback_data="dispatcher_get_my_loads"
    ),
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
    markup = InlineKeyboardMarkup(row_width=5)
    for index, load_id in enumerate(indices, start=1):
        print("Load Data: ", load_id)
        markup.add(
            InlineKeyboardButton(
                text=str(index),
                callback_data=f"driver_request_to_client:{load_id}",
            )
        )
    return markup


def client_confirmation_btn(transaction_uuid):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="✅ Tasdiqlash",
            callback_data=f"confirm_load_splitting_part{transaction_uuid}",
        ),
    )
    markup.add(
        InlineKeyboardButton(
            text="🚫 Yuk yetib kelmadi!", callback_data="deny_confirmation"
        )
    )
    return markup


def successfully_delivered_btn(transaction_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Yukni yetqazib berildi!",
            callback_data=f"qqq:{transaction_id}",
        )
    )
    return markup


contact_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Telefon raqamimni jo'natish", request_contact=True)]
    ],
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
            text=f"Yuk tashuvchini tanlash",
            callback_data=f"driver_get_load_{driver_id}",
        )
    )
    return keyboard


def get_buttons_by_role(role):
    user_button = {
        "driver": driver_buttons,
        "client": get_clients_buttons(0),
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
            text="Keyingisi ⏩",
            callback_data="next_to_receiver_phone_number",
        )
    else:
        next_btn = InlineKeyboardButton(
            text="Keyingisi ⏩",
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
    InlineKeyboardButton(text="Asosiy menyu", callback_data="main_menu")
)
