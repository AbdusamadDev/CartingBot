from aiogram import executor
import logging
import asyncio

from bot.conf import dp
from bot.register import (
    register_registration_handlers,
    register_dispatcher_handlers,
    register_commands_handlers,
    register_client_handlers,
    register_driver_handlers,
    register_global_handlers,
    register_login_handlers,
)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(register_registration_handlers(dp))
    asyncio.run(register_dispatcher_handlers(dp))
    asyncio.run(register_commands_handlers(dp))
    asyncio.run(register_client_handlers(dp))
    asyncio.run(register_global_handlers(dp))
    asyncio.run(register_driver_handlers(dp))
    asyncio.run(register_login_handlers(dp))
    executor.start_polling(dp, skip_updates=True)
