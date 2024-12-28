import os
from enum import Enum

from dotenv import load_dotenv


class Modes(Enum):
    test = 'test'
    relise = 'relise'


class Config():
    '''Настройки бота'''

    def __init__(self, mode=Modes.test.value) -> None:
        self.mode = mode
        load_dotenv()


    def get_token(self):
        '''Токен бота'''
        return os.getenv('TOKEN')


    def get_admin_id(self):
        '''ID владельца бота'''
        return int(os.getenv('ADMIN_ID'))


    def get_db_conneciton(self):
        '''Возвращает подключение к бд'''
        return 'sqlite:///core/utils/database/Xakum.db'


    def get_max_warnings(self):
        '''Максимальное количество предупреждений'''
        return 3


conf = Config()
