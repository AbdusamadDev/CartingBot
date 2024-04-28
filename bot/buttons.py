from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


client_buttons = InlineKeyboardMarkup(row_width=2)
client_btn = [
    InlineKeyboardButton(text="Show Loads", callback_data="show_my_load"),
    InlineKeyboardButton(text="Add Load", callback_data="add_load"),
    InlineKeyboardButton(text="My profile", callback_data="profile_view"),
]
client_buttons.add(*client_btn)


driver_buttons = InlineKeyboardMarkup()
driver_btn = [
    InlineKeyboardButton(text="Show my Loads", callback_data="show_load"),
    InlineKeyboardButton(text="My profile", callback_data="profile_view"),
]
driver_buttons.add(*driver_btn)

dispatcher_buttons = InlineKeyboardMarkup()
dispatcher_btn = [
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


# Define the function to generate district selection buttons
def get_district_selection_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    districts = [
        "District A",
        "District B",
        "District C",
        "District D",
    ]  # Add your districts here
    for district in districts:
        keyboard.add(
            InlineKeyboardButton(
                text=district,
                callback_data=f"district_{district.lower().replace(' ', '_')}",
            )
        )
    return keyboard
