from datetime import datetime

from sqlalchemy import Column, BigInteger, Boolean, DateTime

from core.utils.database.base_db_parametrs import Base, Session


class UsersTable():
    Session = Session


    class Users(Base):
        __tablename__ = 'users'

        id = Column(BigInteger(), primary_key=True)
        admin = Column(Boolean())
        can_use_banword = Column(Boolean())
        warnings = Column(BigInteger())
        baned = Column(Boolean())
        ban_to = Column(DateTime())
        bans_count = Column(BigInteger())


    # -------------------------
    # ---------- add ----------
    # -------------------------


    def add_user(
            self,
            id: int,
            admin: bool = False,
            can_use_banword: bool = False,
            warnings: int = 0,
            baned: bool = False,
            ban_to: datetime = None,
            bans_count: int = 0,
    ) -> None:
        '''
        Добавление записи о пользователе в бд

        :param id: айди пользователя в тг
        :param admin: является ли админом
        :param can_use_banword: может ли писать банворды
        :param warnings: кол-во предупреждений
        :param baned: забанен или нет
        :param ban_to: забанен до какой даты
        :param bans_count: сколько раз был забанен
        '''

        with self.Session() as session:
            admin = self.Users(
                id=id,
                admin=admin,
                can_use_banword=can_use_banword,
                warnings=warnings,
                baned=baned,
                ban_to=ban_to,
                bans_count=bans_count,
            )
            session.add(admin)
            session.commit()


    # -------------------------
    # ---------- edit ---------
    # -------------------------


    def edit_user_warnings_count(
            self,
            id: int,
            new_count: int = 0
    ) -> None:
        '''
        Изменяет количество предупреждения пользователя

        :param id: айди пользователя
        :param new_count: новое количество
        '''
        with self.Session() as session:
            session.query(self.Users).filter(
                self.Users.id == int(id)
            ).update({
                self.Users.warnings: new_count
            })
            session.commit()


    def edit_user_admin(
            self,
            id: int,
            admin: bool = False
    ) -> None:
        '''
        Изменяет статус пользователя (админ или не админ)

        :param id: айди пользователя в тг
        :param admin: является ли админом
        '''
        with self.Session() as session:
            session.query(self.Users).filter(
                self.Users.id == int(id)
            ).update({
                self.Users.admin: admin
            })
            session.commit()


    def edit_user_can_use_banwords(
            self,
            id: int,
            can_use_banword: bool = False
    ) -> None:
        '''
        Изменяет статус пользователя (может использовать банворды или нет)

        :param id: айди пользователя в тг
        :param can_use_banword: может использовать банворды или нет
        '''
        with self.Session() as session:
            session.query(self.Users).filter(
                self.Users.id == int(id)
            ).update({
                self.Users.can_use_banword: can_use_banword
            })
            session.commit()


    def edit_user_bans(
            self,
            id: int,
            bans: int = 0
    ) -> None:
        '''
        Изменяет количество банов пользователя

        :param id: айди пользователя в тг
        :param bans: новое кол-во банов
        '''
        with self.Session() as session:
            session.query(self.Users).filter(
                self.Users.id == int(id)
            ).update({
                self.Users.bans: int(bans)
            })
            session.commit()


    def edit_user_baned(
            self,
            id: int,
            baned: bool = False
    ) -> None:
        '''
        Изменяет состояние бана пользователя

        :param id: айди пользователя в тг
        :param baned: забанен или нет
        '''
        with self.Session() as session:
            session.query(self.Users).filter(
                self.Users.id == int(id)
            ).update({
                self.Users.baned: baned
            })
            session.commit()


    def edit_user_baned_expiration(
            self,
            id: int,
            baned_to: datetime
    ) -> None:
        '''
        Изменяет состояние бана пользователя

        :param id: айди пользователя в тг
        :param baned_to: дата окончания бана
        '''
        with self.Session() as session:
            session.query(self.Users).filter(
                self.Users.id == int(id)
            ).update({
                self.Users.ban_to: baned_to
            })
            session.commit()


    # -------------------------
    # ---------- get ----------
    # -------------------------


    def get_user(
            self,
            id: int
    ) -> Users | None:
        '''
        Возвращает запись о пользователе

        :param id: айди пользователя
        '''

        with self.Session() as session:
            return session.query(self.Users).filter(
                self.Users.id == id
            ).first()


    def get_all_users(self) -> list[Users]:
        '''Возвращает список всех пользователей'''

        with self.Session() as session:
            return session.query(self.Users).all()


    def get_users_to_unban(self) -> list[Users]:
        '''Возвращает список пользовательей с истекшим баном'''

        with self.Session() as session:
            return session.query(self.Users).filter(
                self.Users.baned == True,
                self.Users.ban_to < datetime.now()
            ).all()


    # -------------------------
    # ---------- del ----------
    # -------------------------


    def del_user(
            self,
            id: int
    ) -> None:
        '''Удаляет пользователя из бд'''

        with self.Session() as session:
            session.query(self.Users).filter(
                self.Users.id == int(id)
            ).delete()
            session.commit()
