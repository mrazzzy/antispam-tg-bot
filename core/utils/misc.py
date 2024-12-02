from datetime import datetime

from typing import List

from aiogram.types import Message

from loguru import logger

from helper import bot


async def try_delete(
    msg: List[Message] | Message
):
    '''Пытается удалить сообщение'''
    if isinstance(msg, list):
        for i in msg:
            await try_delete(i)
        return
    try:
        await msg.delete()
    except Exception as e:
        logger.warning(f'Сообщение от пользователя не было удалено по причине {e}')


async def try_send(
        chat_id: int,
        text: str
):
    '''Пытается отправить сообщение'''
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.warning(f'Не удалось отправить сообщение по причине {e}')


async def try_ban(
        chat_id: int,
        user_id: int,
        until_date: datetime
):
    '''Пытается забанить пользователя'''
    try:
        await bot.ban_chat_member(chat_id=chat_id, user_id=user_id, until_date=until_date)
        logger.info(f'Пользователь {user_id} забанен в чате {chat_id} до {until_date.strftime("%d.%m.%Y  %H:%M:%S")}')
    except Exception as e:
        logger.warning(
            f'Не удалось забанить пользователя {user_id} в чате {chat_id} до {until_date.strftime("%d.%m.%Y  %H:%M:%S")}'
            f' по причине {e}'
        )


def is_int(string: str | List[str]) -> bool:
    '''
    Проверяет, является ли строка числом

    :param string: Проверяемая строка или список проверяемых строк
    '''
    try:
        if isinstance(string, list):
            for i in string:
                num = int(i)
                num += 1
        else:
            num = int(string)
        num += 1
        return True
    except ValueError:
        return False


def is_float(string: str | List[str]) -> bool:
    '''
    Проверяет, является ли строка числом

    :param string: Проверяемая строка или список проверяемых строк
    '''
    try:
        if isinstance(string, list):
            for i in string:
                num = float(i)
                num += 1
        else:
            num = float(string)
        num += 1
        return True
    except ValueError:
        return False


def set_loggers():
    logger.add(
        'logs/{time}.log',
        level='INFO',
        backtrace=True,
        diagnose=True,
        rotation='00:00',
        retention='1 week',
        catch=True
    )
    logger.add(
        'errors/{time}.log',
        level='ERROR',
        backtrace=True,
        diagnose=True,
        rotation='00:00',
        retention='1 week',
        catch=True
    )
