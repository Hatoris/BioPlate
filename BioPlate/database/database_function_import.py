from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import create_engine, engine, MetaData, Table
import os



Base = declarative_base()

def db_path(db_name):
    """

    :param db_name: String, name of the db file
    :return: abspath of database in function of calling directory
    """
    if os.path.basename(os.getcwd()) == 'database':
        database = rf"{os.path.abspath(os.path.join('DBFiles', db_name))}"
    elif os.path.basename(os.getcwd()) == 'BioPlate':
        database = rf"{os.path.abspath(os.path.join('database/DBFiles', db_name))}"
    else:
        database = None
    return database


def create_table(engine):
    """
    This function is used to return a sqlalchemy session

    :param engine: 'sqlite:////./plate.db'
    :return: a sqlalchemy session object
    """

    engine = create_engine(engine)
    Base.metadata.create_all(engine)

def create_session(engine):
    """
    This function is used to return a sqlalchemy session

    :param engine: 'sqlite:////./plate.db'
    :return: a sqlalchemy session object
    """

    engine = create_engine(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    DBSession.bind = engine
    session = DBSession()
    return session

