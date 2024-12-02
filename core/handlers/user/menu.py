from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message

from loguru import logger

from core.utils.database.database import db
from core.utils.filters import Monitoring, UserMessage
from core.utils.misc import try_send, try_ban

from config import conf

r = Router()


@r.message(F.text, Monitoring(), UserMessage())
async def get_group_msg(msg: Message):
    user = db.get_user(msg.from_user.id)
    if user is None:
        db.add_user(msg.from_user.id)
        user = db.get_user(msg.from_user.id)

    logger.debug('Чекаем на банворд')
    if user.can_use_banword:
        return

    chat = db.get_chat(msg.chat.id)
    logger.debug('Получаем список банвордов')
    banwords = db.get_all_banwords()
    ban = False

    logger.debug('Проходим по списку банвордов')
    for banword in banwords:
        if banword.content in msg.text.lower():
            ban = True
            if banword.antiban:
                ban = False
                break

    if ban:
        await msg.delete()
        msg_text = f'@{msg.from_user.username}, Вы нарушили правила беседы, использовав запрещенные слова. '
        ban_time = max(1, user.bans_count * 3)

        if user.warnings >= conf.get_max_warnings():
            msg_text += f'Поскольку Вы сделали это уже в {user.warnings} раз, Вы отправляетесь в бан на {ban_time} суток.'
            await try_send(msg.from_user.id, msg_text)
            await msg.answer(msg_text)
            chats = db.get_all_monitoring_chats()

            for chat in chats:
                await try_ban(chat.id, user.id, datetime.now() + timedelta(ban_time))

            db.edit_user_warnings_count(user.id, 0)
            db.edit_user_baned(msg.from_user.id)
            return

        msg_text += (
            f'Это Ваше {user.warnings + 1} предупреждение, на {conf.get_max_warnings() + 1} '
            f'Вы будете забанены на {ban_time} суток. Постарайтесь впредь быть аккуратнее.'
        )
        await msg.answer(msg_text)
        db.edit_user_warnings_count(user.id, user.warnings + 1)
