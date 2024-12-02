from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import Config

conf = Config()
engine = create_engine(conf.get_db_conneciton(), echo=False, isolation_level="AUTOCOMMIT", pool_pre_ping=True)
Session = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
