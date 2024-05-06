from aiogram import executor
import logging

from bot.database import create_table, clear_database
from bot.conf import dp
from bot.register import (
    register_registration_handlers,
    # register_dispatcher_handlers,
    register_commands_handlers,
    register_client_handlers,
    register_driver_handlers,
    register_global_handlers,
    register_login_handlers,
)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_table()
    # clear_database()
    register_registration_handlers(dp)
    # register_dispatcher_handlers(dp)
    register_commands_handlers(dp)
    register_client_handlers(dp)
    register_global_handlers(dp)
    register_driver_handlers(dp)
    register_login_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
