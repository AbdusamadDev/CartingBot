from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationState(StatesGroup):
    phonenumber = State()
    sms_code = State()
    role = State()
    password = State()


class LoadCreationState(StatesGroup):
    image = State()
    product_name = State()
    product_info = State()
    product_type = State()
    product_count = State()
    region = State()
    district = State()
    address = State()
    receiver_phone_number = State()
    date_delivery = State()
    from_location = State()


class DeliveryRequestState(StatesGroup):
    driver_id = State()
    load_id = State()


class TokenStorageState(StatesGroup):
    token = State()


class LoginState(StatesGroup):
    phonenumber = State()
    password = State()


class LoadDetailsState(StatesGroup):
    loads = State()
    page = State()
    max_length = State()
