from sqlalchemy import Column, String, Boolean

from core.utils.database.base_db_parametrs import Base, Session


class ChatsTable():
    Session = Session


    class Chats(Base):
        __tablename__ = 'Chats'

        id = Column(String(), primary_key=True)
        chat_name = Column(String())
        monitoring = Column(Boolean())


    # -------------------------
    # ---------- add ----------
    # -------------------------


    def add_chat(
            self,
            id: int,
            chat_name: str,
            monitoring: bool = True,
    ) -> None:
        '''
        Добавление записи о чате в бд

        :param id: айди чата
        :param chat_name: название чата, заголово
        :param monitoring: отслеживать ли чат на наличие банвордов
        '''

        with self.Session() as session:
            chat = self.Chats(
                id=int(id),
                chat_name=chat_name,
                monitoring=monitoring,
            )
            session.add(chat)
            session.commit()


    # -------------------------
    # ---------- edit ---------
    # -------------------------


    def edit_chat_checking(
            self,
            id: int,
            checking: bool = True
    ) -> None:
        '''
        Изменить проверку чата

        :param id: айди чата
        :param checking: чекать или нет
        '''
        with self.Session() as session:
            session.query(self.Chats).filter(
                self.Chats.id == id
            ).update({
                self.Chats.monitoring: checking
            })
            session.commit()


    # -------------------------
    # ---------- get ----------
    # -------------------------


    def get_chat(
            self,
            id: str
    ) -> Chats | None:
        '''
        Возвращает запись о чате

        :param id: айди чата
        '''

        with self.Session() as session:
            return session.query(self.Chats).filter(
                self.Chats.id == id
            ).first()


    def get_all_chats(self) -> list[Chats]:
        '''Возвращает список всех чатов'''

        with self.Session() as session:
            return session.query(self.Chats).all()


    def get_all_monitoring_chats(self) -> list[Chats]:
        '''Список всех чатов, где проверяется на банворды'''

        with self.Session() as session:
            return session.query(self.Chats).filter(
                self.Chats.monitoring == True
            ).all()


    # -------------------------
    # ---------- del ----------
    # -------------------------


    def del_chat(
            self,
            id: str
    ) -> None:
        '''Удаляет чат из бд'''

        with self.Session() as session:
            session.query(self.Chats).filter(
                self.Chats.id == int(id)
            ).delete()
            session.commit()
