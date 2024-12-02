import asyncio

from art import tprint
from loguru import logger

from core.utils.midlewares import UpdateLogger
from core.utils.misc import set_loggers

from helper import bot, dp


async def on_startup():
    bot_info = await bot.get_me()
    tprint(f'@{bot_info.username}    online')
    logger.warning(f'bot info: @{bot_info.username} {bot_info.first_name} {bot_info.id}')


def include_admin_routers():
    from core.handlers.admin import (
        menu,
    )
    dp.include_routers(
        menu.r,
    )


def include_user_routers():
    from core.handlers.user import (
        menu,
    )
    dp.include_routers(
        menu.r,
    )


async def main():
    set_loggers()
    include_admin_routers()
    include_user_routers()

    dp.update.middleware(UpdateLogger())
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
