from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


notifications_button = InlineKeyboardButton(
    text="Show Notifications",
    callback_data="notifications",
)

client_buttons = InlineKeyboardMarkup(row_width=2)
client_btn = [
    notifications_button,
    InlineKeyboardButton(text="Show Loads", callback_data="show_my_load"),
    InlineKeyboardButton(text="Add Load", callback_data="add_load"),
    InlineKeyboardButton(text="My profile", callback_data="profile_view"),
]
client_buttons.add(*client_btn)


driver_buttons = InlineKeyboardMarkup()
driver_btn = [
    notifications_button,
    InlineKeyboardButton(text="Show my Loads", callback_data="show_load"),
    InlineKeyboardButton(text="My profile", callback_data="profile_view"),
]
driver_buttons.add(*driver_btn)

dispatcher_buttons = InlineKeyboardMarkup()
dispatcher_btn = [
    notifications_button,
    InlineKeyboardButton(
        text="Show All loads", callback_data="dispatcher_show_all_loads"
    ),
    InlineKeyboardButton(
        text="Request GET Driver Load [further]",
        callback_data="request_dispatcher_to_driver",
    ),
    InlineKeyboardButton(text="Show Drivers", callback_data="dispatcher_show_drivers"),
    InlineKeyboardButton(text="Show my Loads", callback_data="dispatcher_get_my_loads"),
    InlineKeyboardButton(text="My profile", callback_data="profile_view"),
]
dispatcher_buttons.add(*dispatcher_btn)


def get_loads_button(indices):
    keyboard = InlineKeyboardMarkup()
    for load_id in indices:
        keyboard.add(
            InlineKeyboardButton(
                text=f"Request for load: {load_id}",
                callback_data=f"dispatcher_driver_delivery_request_{load_id}",
            )
        )
    return keyboard


def driver_my_loads_buttons(indices):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for load_id, client_id in indices:
        keyboard.add(
            InlineKeyboardButton(
                text=f"Request for {load_id}",
                callback_data=f"driver_show_load_{load_id}_{client_id}",
            )
        )
    return keyboard


def get_driver_buttons(indices):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for driver_id, fullname in indices:
        keyboard.add(
            InlineKeyboardButton(
                text=f"Request for {fullname}",
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


def get_regions_button(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    print(data)
    for region in data:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{region['name']}",
                callback_data=f"fetch_districts_of_region_{region['pk']}",
            )
        )
    return keyboard


def get_districts_button(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    print("DATA: ", data["district"])
    for district in data["district"]:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{district['name']}",
                callback_data=f"add_district_to_state_{district['pk']}",
            )
        )
    return keyboard
