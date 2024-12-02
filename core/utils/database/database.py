from core.utils.database import (
    chats,
    users,
    banwords
)
from core.utils.database.base_db_parametrs import Base, engine


class DataBase(
    users.UsersTable,
    chats.ChatsTable,
    banwords.BanWordsTable
):
    '''
    Класс для работы с базой данных
    '''
    Base.metadata.create_all(engine, checkfirst=True)


db = DataBase()
