from sqlalchemy import Column, Boolean, String

from core.utils.database.base_db_parametrs import Base, Session


class BanWordsTable():
    Session = Session


    class BanWords(Base):
        __tablename__ = 'BanWords'

        content = Column(String(), primary_key=True)
        antiban = Column(Boolean())


    # -------------------------
    # ---------- add ----------
    # -------------------------


    def add_banword(
            self,
            content: str,
            antiban: bool = False
    ) -> None:
        '''
        Добавление записи о банворде в бд

        :param content: текст банворда
        :param antiban: не банить, если есть, даже при наличии банворда
        '''

        with self.Session() as session:
            banword = self.BanWords(
                content=content,
                antiban=antiban
            )
            session.add(banword)
            session.commit()


    # -------------------------
    # ---------- get ----------
    # -------------------------


    def get_banword(
            self,
            content: str
    ) -> BanWords | None:
        '''
        Возвращает запись о банворде

        :param content: банворд
        '''

        with self.Session() as session:
            return session.query(self.BanWords).filter(
                self.BanWords.content == content
            ).first()


    def get_all_banwords(self) -> list[BanWords]:
        '''Возвращает список всех админов'''

        with self.Session() as session:
            return session.query(self.BanWords).all()


    # -------------------------
    # ---------- del ----------
    # -------------------------


    def del_banword(
            self,
            content: str
    ) -> None:
        '''Удаляет банворд из бд'''

        with self.Session() as session:
            session.query(self.BanWords).filter(
                self.BanWords.content == content
            ).delete()
            session.commit()
