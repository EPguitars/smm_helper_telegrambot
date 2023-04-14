# pylint: disable=broad-exception-caught
"""
All operations with db in this module 
SQLAlchemy used as orm
"""


import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine.url import URL
from sqlalchemy import select
import colorama
from colorama import Fore, Style

Session = orm.sessionmaker()

DATABASE = {
    'drivername': 'sqlite',
    'database': 'database.db'
}

engine = sa.create_engine(URL.create(**DATABASE))
Base = orm.declarative_base()
colorama.init(autoreset=True)


class Categories(Base):
    """
    Mapper for table "categories"
    """
    __table__ = sa.Table('categories', Base.metadata, autoload_with=engine)

class Channels(Base):
    """
    Mapper for table "channels"
    """
    __table__ = sa.Table('channels', Base.metadata, autoload_with=engine)


def get_categories() -> list: 
    """ 
    Возвращает список категорий из бд 
    """
    session = Session(bind=engine)
    
    dbdata = select(Categories)
    result = [x.name for x in session.scalars(dbdata)]
    session.close()
    

    return result


def add_category(category_name: str) -> None:
    """
    Добавляет категорию в бд
    """
    session = Session(bind=engine)

    if session.query(Categories.name).filter_by(name=category_name).first() is None:

        category = Categories(name=category_name)
        session.add(category)
    else:
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}Категория {category_name} уже существует!")        
    
    session.commit()
    session.close()

def delete_category(category_name: str) -> None:
    """
    Удаляет категорию из бд
    """
    session = Session(bind=engine)
    record = session.query(Categories).filter_by(name=category_name).first()

    if record is not None:
        session.delete(record)

    session.commit()
    session.close()
    

def get_channels(category_name: str) -> list:
    session = Session(bind=engine)

    dbdata = select(Channels).filter_by(category = category_name)
    result = [x.link for x in session.scalars(dbdata)]
    session.close()

    return result

def add_channel(category_name: str, link: str) -> None:
    session = Session(bind=engine)

    record = session.query(Channels).filter_by(link=link).first()

    if record is None:
        channel = Channels(link=link, category=category_name)
        session.add(channel)
        session.commit()
    
    else:
        print(f"{Fore.CYAN}{Style.BRIGHT}ALREADY SATISFIED")

