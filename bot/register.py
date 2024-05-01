from aiogram import Dispatcher, types
from bot.states import *

from bot.roles.client import (
    process_receiver_phone_number,
    client_show_my_load_handler,
    process_add_load_callback,
    process_district_callback,
    process_region_callback,
    process_choice_handler,
    process_image_handler,
    process_product_count,
    process_product_name,
    process_product_info,
)
from bot.roles.dispatcher import (
    dispatcher_show_all_loads_handler,
    dispatcher_get_my_loads_handler,
    request_for_load_profile_view,
    ask_for_which_load_handler,
    show_all_drivers_handler,
    request_for_load,
)
from bot.globals import (
    main_menu_callback_handler,
    get_notifications_handler,
    profile_view_callback,
)
from bot.auth.registration_handlers import (
    share_number_for_registration,
    process_role_callback,
    process_phonenumber,
    process_password,
    process_sms_code,
)
from bot.auth.login_handlers import share_number_for_login
from bot.roles.driver import show_my_loads
from bot.commands import start_handler


def register_client_handlers(dp: Dispatcher):
    """
    Registers all necessary handlers for client interactions within the bot.

    This function sets up callback query handlers and message handlers for various states
    and interactions related to load creation and management.

    Parameters:
    - dp: Dispatcher
        The Aiogram Dispatcher to which the handlers are registered.
    """

    # Register callback query handlers for load creation flow
    callback_query_handlers = [
        ("show_my_load", None, client_show_my_load_handler),
        ("add_load", None, process_add_load_callback),
        ("region:", LoadCreationState.region, process_region_callback),
        ("choice", LoadCreationState.product_type, process_choice_handler),
        ("district", LoadCreationState.district, process_district_callback),
    ]
    for data_contains, state, callback in callback_query_handlers:
        dp.register_callback_query_handler(
            callback,
            lambda query, data_contains=data_contains: query.data.startswith(
                data_contains
            ),
            state=state,
        )

    # Register message handlers for load creation flow
    message_handlers = [
        (LoadCreationState.image, ["photo"], process_image_handler),
        (LoadCreationState.product_name, None, process_product_name),
        (LoadCreationState.product_info, None, process_product_info),
        (LoadCreationState.product_count, None, process_product_count),
        (LoadCreationState.receiver_phone_number, None, process_receiver_phone_number),
    ]
    for state, content_types, callback in message_handlers:
        dp.register_message_handler(
            callback,
            state=state,
            content_types=content_types if content_types else types.ContentTypes.TEXT,
        )


def register_driver_handlers(dp: Dispatcher):
    """
    A coroutine for registering all driver-related query and message handlers.

    This function is intended to set up handlers that respond to driver-specific queries and messages
    within an asynchronous application. It should be called to initialize and start the event loop
    handling all registered driver activities. Currently, this function does not implement any handlers
    and serves as a placeholder for future development.

    Parameters:
    - dp (Dispatcher): The Dispatcher instance from aiogram to which the handlers will be registered.

    There are no return values for this function as it is expected to operate asynchronously and
    register handlers that will be invoked by the aiogram event loop.
    """
    dp.register_callback_query_handler(
        text_contains="show_load", callback=show_my_loads
    )
    dp.register_callback_query_handler(
        text_contains="driver_show_load_", callback=show_my_loads
    )


def register_dispatcher_handlers(dp: Dispatcher):
    """
    Registers dispatcher-specific callback query handlers for the bot.

    This function sets up a series of callback query handlers specifically designed for dispatcher
    interactions. These handlers cover functionalities such as viewing dispatcher's own loads, showing
    all drivers, showing all loads, handling delivery requests, and more. Each handler is associated
    with a specific command or action within the dispatcher's role, facilitating the management and
    interaction with loads and drivers.

    Parameters:
    - dp (Dispatcher): The Aiogram Dispatcher instance to which the callback query handlers are registered.

    There are no return values for this function as it operates by side-effect, registering handlers
    with the dispatcher to handle future callback query events based on specific text patterns.
    """

    # Grouping callback query handlers by common patterns for clarity
    dispatcher_handlers = [
        ("dispatcher_get_my_loads", None, dispatcher_get_my_loads_handler),
        ("dispatcher_show_drivers", None, show_all_drivers_handler),
        ("dispatcher_show_all_loads", None, dispatcher_show_all_loads_handler),
        ("dispatcher_driver_delivery_request_", DeliveryRequestState.load_id, None),
        ("driver_get_load_", None, ask_for_which_load_handler),
        ("driver_get_loads_profile_view:", None, request_for_load_profile_view),
        ("request_dispatcher_to_driver", None, request_for_load),
    ]

    # Registering handlers using a loop to reduce redundancy
    for text_contains, state, callback in dispatcher_handlers:
        dp.register_callback_query_handler(
            callback=callback, text_contains=text_contains, state=state
        )


def register_global_handlers(dp: Dispatcher):
    """
    Registers global callback query handlers for the bot.

    This function sets up handlers for global actions such as accessing the main menu,
    viewing notifications, and accessing the profile view. These handlers are not specific
    to any user role or state and can be triggered from anywhere within the bot's conversation flow.

    Parameters:
    - dp (Dispatcher): The Aiogram Dispatcher instance to which the global handlers are registered.

    There are no return values for this function as it operates by side-effect, registering handlers
    with the dispatcher to handle future events.
    """
    global_handlers = [
        ("main_menu", main_menu_callback_handler),
        ("notifications", get_notifications_handler),
        ("profile_view", profile_view_callback),
    ]

    for text, callback in global_handlers:
        dp.register_callback_query_handler(callback=callback, text_contains=text)


def register_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(
        state=RegistrationState.phonenumber, callback=process_phonenumber
    )
    dp.register_message_handler(
        state=RegistrationState.sms_code, callback=process_sms_code
    )
    dp.register_message_handler(
        state=RegistrationState.password, callback=process_password
    )
    dp.register_message_handler(
        content_types=types.ContentType.CONTACT,
        state=RegistrationState.phonenumber,
        callback=share_number_for_registration,
    )
    dp.register_callback_query_handler(
        text=["driver", "client", "dispatcher"],
        state=RegistrationState.role,
        callback=process_role_callback,
    )


def register_login_handlers(dp: Dispatcher):
    dp.register_message_handler(
        state=LoginState.phonenumber,
        content_types=types.ContentType.CONTACT,
        callback=process_phonenumber,
    )
    dp.register_message_handler(
        state=LoginState.phonenumber,
    )
    dp.register_message_handler(state=LoginState.password)


def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(commands=["start"], state="*", callback=start_handler)
