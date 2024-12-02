
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from core.utils.database.database import db
from core.utils.filters import Admin
from core.utils.misc import is_int


r = Router()
r.callback_query.filter(Admin())
r.message.filter(Admin())


@r.message(Command('add_chat'))
async def add_chat(msg: Message):
    chat = db.get_chat(msg.chat.id)

    if chat is not None:
        await msg.reply('Этот чат уже добавлен')
        return

    db.add_chat(msg.chat.id, msg.chat.title)
    await msg.reply('Чат успешно добавлен!')


@r.message(Command('del_chat'))
async def del_chat(msg: Message):
    chat = db.get_chat(msg.chat.id)

    if chat is None:
        await msg.reply('Этот чат еще не добавлен')
        return

    db.del_chat(msg.chat.id)
    await msg.reply('Чат успешно удален!')


@r.message(Command('add_admin'))
async def add_admin(msg: Message):

    if msg.reply_to_message is None:
        await msg.reply('Команда должна быть ответом на сообщение будущего админа')
        return

    user_id = msg.reply_to_message.from_user.id
    user = db.get_user(user_id)

    if user is None:
        db.add_user(user_id)

    db.edit_user_admin(user_id, True)
    await msg.reply('Пользователь успешно стал админом!')


@r.message(Command('del_admin'))
async def del_admin(msg: Message):

    if msg.reply_to_message is None:
        await msg.reply('Команда должна быть ответом на сообщение разжалываемого админа')
        return

    user_id = msg.reply_to_message.from_user.id
    user = db.get_user(user_id)

    if user is None:
        db.add_user(user_id)
        await msg.reply('Пользователь успешно перестал быть админом!')
        return

    db.edit_user_admin(user_id, False)
    await msg.reply('Пользователь успешно перестал быть админом!')


@r.message(Command('banword'))
async def reply_banword(msg: Message):

    if msg.reply_to_message is None:
        await msg.reply('Команда должна быть ответом на сообщение-банворд')
        return

    banword = db.get_banword(msg.reply_to_message.text.lower())
    if banword is not None:
        await msg.reply('Такой банворд уже есть')
        return

    db.add_banword(msg.reply_to_message.text.lower())
    await msg.reply('Банворд добавлен!')


@r.message(Command('add_banword'))
async def add_banword(msg: Message):

    params = msg.text.split()

    if len(params) != 2:
        await msg.reply('Неверное количество параметров команды. Правильный синтаксис - /add_banword <банворд>, без скобок')
        return

    banword = db.get_banword(params[1].lower())
    if banword is not None:
        await msg.reply('Такой банворд уже есть')
        return

    db.add_banword(params[1].lower())
    await msg.reply('Банворд добавлен!')


@r.message(Command('del_banword'))
async def del_banword(msg: Message):
    params = msg.text.split()

    if len(params) != 2:
        await msg.reply('Неверное количество параметров команды. Правильный синтаксис - /add_banword <банворд>, без скобок')
        return

    banword = db.get_banword(params[1].lower())
    if banword is None:
        await msg.reply('Такого банворда еще нет')
        return

    db.del_banword(params[1].lower())
    await msg.reply('Банворд удален!')


@r.message(Command('start_checking'))
async def start_checking(msg: Message):

    if msg.reply_to_message is None:
        await msg.reply('Команда должна быть ответом на сообщение')
        return

    user = db.get_user(msg.from_user.id)
    if user is None:
        db.add_user(msg.from_user.id)

    db.edit_user_can_use_banwords(msg.from_user.id, False)
    await msg.reply('Теперь я слежу за ним')


@r.message(Command('stop_checking'))
async def stop_checking(msg: Message):

    if msg.reply_to_message is None:
        await msg.reply('Команда должна быть ответом на сообщение')
        return

    user = db.get_user(msg.from_user.id)
    if user is None:
        db.add_user(msg.from_user.id)

    db.edit_user_can_use_banwords(msg.from_user.id, True)
    await msg.reply('Больше я за ним не слежу')


@r.message(Command('set_bans'))
async def set_bans(msg: Message):
    params = msg.text.split()

    if len(params) != 2:
        await msg.reply('Неверное количество параметров команды. Правильный синтаксис - /set_bans <кол-во банов>, без скобок')
        return

    if msg.reply_to_message is None:
        await msg.reply('Команда должна быть ответом на сообщение')
        return

    if not is_int(params[1]):
        await msg.reply('Новое количество банов должно быть числом!')
        return

    db.edit_user_bans(msg.reply_to_message.from_user.id, int(params[1]))
    await msg.reply('Изменено!')


@r.message(Command('set_warnings'))
async def set_warnings(msg: Message):
    params = msg.text.split()

    if len(params) != 2:
        await msg.reply(
            'Неверное количество параметров команды. Правильный синтаксис - /set_warnings <кол-во предупреждений>, без скобок'
        )
        return

    if msg.reply_to_message is None:
        await msg.reply('Команда должна быть ответом на сообщение')
        return

    if not is_int(params[1]):
        await msg.reply('Новое количество предупреждений должно быть числом!')
        return

    db.edit_user_warnings_count(msg.reply_to_message.from_user.id, int(params[1]))
    await msg.reply('Изменено!')


@r.message(Command('start_chat_checking'))
async def start_chat_checking(msg: Message):

    chat = db.get_chat(msg.chat.id)
    if chat is None:
        db.add_chat(msg.chat.id, msg.chat.title)

    db.edit_chat_checking(msg.chat.id, True)
    await msg.reply('Теперь я слежу за этим чатом')


@r.message(Command('stop_chat_checking'))
async def stop_chat_checking(msg: Message):

    chat = db.get_chat(msg.chat.id)
    if chat is None:
        db.add_chat(msg.chat.id, msg.chat.title)

    db.edit_chat_checking(msg.chat.id, False)
    await msg.reply('Больше я за этим чатом не слежу')


@r.message(Command('help'))
async def help_comand(msg: Message):
    await msg.reply(
        'Вот список моих команд:\n\n'

        '/add_chat - добавляет чат, в котором была вызвана команда, в базу данных\n'
        '/del_chat - удаляет чат, в котором была вызвана команда, из базы данных\n'
        '/add_admin - делает пользователя, на сообщение которого ответили этой командой, админом\n'
        '/del_admin - делает пользователя, на сообщение которого ответили этой командой, не админом\n'
        '/banword - регистрирует текст сообщения, на которое ответили этой командой, банвордом\n'
        '/add_banword <банворд> - добавляет банворд, указанный после команды, в базу данных. Скобки писать не нужно\n'
        '/del_banword <банворд> - удаляет банворд, указанный после команды, из базы данных. Скобки писать не нужно\n'
        '/start_checking - отслеживать сообщения пользователя, на сообщение которого ответили этой командой, '
        'на наличие банвордов\n'
        '/stop_checking - перестать отслеживать сообщения пользоватля, на сообщение которого ответили этой командой, '
        'на наличие банвордов\n'
        '/set_bans <кол-во банов> - установить количество банов пользовтелю, на сообщение которого ответили\n'
        '/set_warnings <кол-во предупреждений> - установить количество предупреждений пользователю, '
        'на сообщение которого ответили\n'
        '/start_chat_checking - отслеживать чат на банводры\n'
        '/stop_chat_checking - не отслеживать чат на банворды'
    )
