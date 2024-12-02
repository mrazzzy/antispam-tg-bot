from typing import Optional, List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.utils.misc import is_int, is_float
from core.utils.database.database import db
from config import conf


class ChatType(BaseFilter):
    def __init__(self, *chat_types):
        self.chat_types = [*chat_types]

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types


class ContentTypes(BaseFilter):
    def __init__(self, *content_types):
        self.content_types = content_types

    async def __call__(self, message: Message) -> bool:
        return message.content_type in self.content_types


class ReplyToBotMsg(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.reply_to_message is None:
            return False
        return message.reply_to_message.from_user.is_bot


class Monitoring(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        chat = db.get_chat(message.chat.id)
        if chat:
            return chat.monitoring
        return False


class UserMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id is not None


class ChatsIds(BaseFilter):
    def __init__(self, *chats):
        self.chats = chats

    async def __call__(self, message: Message) -> bool:
        return message.chat.id in self.chats


class WordsCount(BaseFilter):
    def __init__(self, count: int):
        self.count = count

    async def __call__(self, message: Message) -> bool:
        words = message.text.split()
        return len(words) == self.count


class GreatAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == conf.get_admin_id()


class Admin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == conf.get_admin_id():
            return True

        user = db.get_user(message.from_user.id)

        if user is None:
            return False

        return user.admin


class IntWords(BaseFilter):
    def __init__(self, indexes: Optional[List[int]] = None):
        self.indexes = indexes


    async def __call__(self, msg: Message) -> bool:

        text = msg.text.replace(',', '.')
        params = text.split()
        numeric = True

        if self.indexes is not None:
            if is_int([params[i] for i in self.indexes]) is False:
                numeric = False

        else:
            if len(params) != 0:
                if is_int(params) is False:
                    numeric = False
            else:
                numeric = is_int(text)

        return numeric


class FloatWords(BaseFilter):
    def __init__(self, indexes: Optional[List[int]] = None):
        self.indexes = indexes


    async def __call__(self, msg: Message) -> bool:

        text = msg.text.replace(',', '.')
        params = text.split()
        numeric = True

        if self.indexes is not None:
            if is_float([params[i] for i in self.indexes]) is False:
                numeric = False

        else:
            if len(params) != 0:
                if is_float(params) is False:
                    numeric = False
            else:
                numeric = is_float(text)

        return numeric
