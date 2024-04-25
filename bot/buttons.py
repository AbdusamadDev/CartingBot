from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


client_buttons = InlineKeyboardMarkup(row_width=2)
client_btn = [
    InlineKeyboardButton(text="Show Loads", callback_data="show_loads"),
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
    InlineKeyboardButton(text="Show All loads"),
    InlineKeyboardButton(text="Request GET Driver Load [further]"),
    InlineKeyboardButton(text="Show Drivers"),
    InlineKeyboardButton(text="Show my loads"),
    InlineKeyboardButton(text="My profile", callback_data="profile_view"),
]
dispatcher_buttons.add(*dispatcher_btn)


def driver_my_loads_buttons(indices):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for load_id, client_id in indices:
        print(load_id, client_id)
        keyboard.add(
            InlineKeyboardButton(
                text=f"Request for {load_id}",
                callback_data=f"driver_show_load_{load_id}_{client_id}",
            )
        )
    return keyboard


def get_buttons_by_role(role):
    user_button = {
        "driver": driver_buttons,
        "client": client_buttons,
        "dispatcher": dispatcher_buttons,
    }
    print("User role button: ", user_button[role])
    return user_button[role]
