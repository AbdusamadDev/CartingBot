from aiogram import Dispatcher, types
from bot.states import *

from bot.roles.client import (
    process_receiver_phone_number,
    client_show_my_load_handler,
    process_add_load_callback,
    process_district_callback,
    process_address_callback,
    client_FINISH_processes,
    process_region_callback,
    process_choice_handler,
    process_image_handler,
    process_product_count,
    process_delivery_date,
    process_product_name,
    process_product_info,
    process_address,
)
from bot.roles.dispatcher import (
    dispatcher_request_to_driver_handler,
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
    confirm_handler,
    reject_handler,
)
from bot.auth.registration_handlers import (
    share_number_for_registration,
    process_role_callback,
    process_phonenumber,
    process_password,
    process_sms_code,
)
from bot.auth.login_handlers import (
    share_number_for_login,
    process_login_handler,
    process_password_login,
)
from bot.roles.driver import (
    finished_delivery_request_to_client,
    driver_to_client_request_handler,
    show_all_loads_for_driver,
    load_pagination_callback,
    load_details_callback,
    show_my_loads,
)
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
        ("district", LoadCreationState.district, process_district_callback),
        ("choice", LoadCreationState.product_type, process_choice_handler),
        ("confirm_load_splitting_part", None, client_FINISH_processes),
        ("region:", LoadCreationState.region, process_region_callback),
        ("retry_add_load", None, process_add_load_callback),
        ("show_my_load", None, client_show_my_load_handler),
        ("add_load", None, process_add_load_callback),
        (
            "next_to_receiver_phone_number",
            LoadCreationState.district,
            process_address_callback,
        ),
    ]
    for data_contains, state, callback in callback_query_handlers:
        dp.register_callback_query_handler(
            callback,
            lambda query, data_contains=data_contains: query.data.startswith(
                data_contains
            ),
            state=state,
        )

    dp.register_callback_query_handler(
        text_contains="deny_confirmation", callback=reject_handler
    )
    # Register message handlers for load creation flow
    message_handlers = [
        (LoadCreationState.receiver_phone_number, None, process_receiver_phone_number),
        (LoadCreationState.date_delivery, None, process_delivery_date),
        (LoadCreationState.product_count, None, process_product_count),
        (LoadCreationState.product_name, None, process_product_name),
        (LoadCreationState.product_info, None, process_product_info),
        (LoadCreationState.image, ["photo"], process_image_handler),
        (LoadCreationState.address, None, process_address),
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
        text_contains="load_details", callback=load_details_callback
    )
    dp.register_callback_query_handler(
        text_contains="show_load", callback=show_my_loads
    )
    dp.register_callback_query_handler(
        text_contains="driver_show_load_", callback=show_my_loads
    )
    dp.register_callback_query_handler(
        text="show_all_driver_loads", callback=show_all_loads_for_driver
    )
    dp.register_callback_query_handler(
        text_contains="driver_request_to_client",
        callback=driver_to_client_request_handler,
    )
    dp.register_callback_query_handler(
        text_contains="driver_successfully_delivered",
        callback=finished_delivery_request_to_client,
    )
    dp.register_callback_query_handler(
        text_contains="decline_request", callback=reject_handler
    )
    dp.register_callback_query_handler(
        load_pagination_callback,
        text_contains="load_pagination:previous:",
        state="*",
    )
    dp.register_callback_query_handler(
        load_pagination_callback,
        text_contains="load_pagination:next:",
        state="*",
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
        ("driver_get_loads_profile_view:", None, request_for_load_profile_view),
        ("dispatcher_show_all_loads", None, dispatcher_show_all_loads_handler),
        ("dispatcher_get_my_loads", None, dispatcher_get_my_loads_handler),
        ("dispatcher_show_drivers", None, show_all_drivers_handler),
        ("request_dispatcher_to_driver", None, request_for_load),
        ("driver_get_load_", None, ask_for_which_load_handler),
        (
            "dispatcher_driver_delivery_request_",
            DeliveryRequestState.load_id,
            dispatcher_request_to_driver_handler,
        ),
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
    dp.register_callback_query_handler(
        text_contains=["confirm_request"],
        callback=confirm_handler,
    )


def register_registration_handlers(dp: Dispatcher):
    """
    Registers handlers for the registration process of users.

    This function sets up message handlers for different stages of the registration process, including
    phone number submission, SMS code verification, and password setting. It also registers a handler
    for receiving a contact as a phone number and a callback query handler for selecting the user's role
    (driver, client, dispatcher).

    Parameters:
    - dp (Dispatcher): The Aiogram Dispatcher instance to which the handlers are registered.

    There are no return values for this function as it operates by side-effect, registering handlers
    with the dispatcher to handle future events related to user registration.
    """
    # Register a message handler for phone number submission in the registration process
    dp.register_message_handler(
        state=RegistrationState.phonenumber, callback=process_phonenumber
    )
    # Register a message handler for SMS code verification during registration
    dp.register_message_handler(
        state=RegistrationState.sms_code, callback=process_sms_code
    )
    # Register a message handler for setting a password in the registration process
    dp.register_message_handler(
        state=RegistrationState.password, callback=process_password
    )
    # Register a message handler for receiving a contact as a phone number during registration
    dp.register_message_handler(
        content_types=types.ContentType.CONTACT,
        state=RegistrationState.phonenumber,
        callback=share_number_for_registration,
    )
    # Register a callback query handler for selecting the user's role during registration
    dp.register_callback_query_handler(
        text=["driver", "client", "dispatcher"],
        state=RegistrationState.role,
        callback=process_role_callback,
    )


def register_login_handlers(dp: Dispatcher):
    dp.register_message_handler(
        state=LoginState.phonenumber,
        content_types=types.ContentType.CONTACT,
        callback=share_number_for_login,
    )
    dp.register_message_handler(
        state=LoginState.phonenumber, callback=process_login_handler
    )
    dp.register_message_handler(
        state=LoginState.password, callback=process_password_login
    )


def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(commands=["start"], state="*", callback=start_handler)
