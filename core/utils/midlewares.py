from typing import Callable, Dict, Any, Awaitable
from time import perf_counter

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from loguru import logger


class UpdateLogger(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        start_time = perf_counter()
        if event.message:
            msg_content_type = event.message.content_type
            event_type = f'сообщение({msg_content_type})'
            event_text = event.message.caption if msg_content_type == 'photo' else event.message.text
        elif event.callback_query:
            event_type = 'колбек'
            event_text = event.callback_query.data
        else:
            event_type = 'неизвестный'
            event_text = 'неизвестный'

        logger.info(f'Пришел апдейт типа {event_type} от @{data["event_from_user"].username} с текстом {event_text}')
        result = await handler(event, data)

        end_time = perf_counter()
        logger.info(f'Апдейт от @{data["event_from_user"].username} обработан за {round(end_time - start_time, 3)} секунд')
        return result
