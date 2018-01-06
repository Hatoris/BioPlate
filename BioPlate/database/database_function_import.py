from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
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
    elif os.path.basename(os.getcwd()) == 'tests':
        database = rf"{os.path.abspath(os.path.join(os.pardir, os.path.join('BioPlate/database/DBFiles', db_name)))}"
    else:
        database = None
    return database


def create_table(sqlalchemypath):
    """
    This function is used to return a sqlalchemy session

    :param sqlalchemypath: 'sqlite:////./plate.db'
    :return: a sqlalchemy session object
    """

    my_engine = create_engine(sqlalchemypath)
    Base.metadata.create_all(my_engine)


def create_session(sqlalchemypath):
    """
    This function is used to return a sqlalchemy session

    :param sqlalchemypath: 'sqlite:////./plate.db'
    :return: a sqlalchemy session object
    """

    my_engine = create_engine(sqlalchemypath)
    Base.metadata.bind = my_engine
    db_session = sessionmaker(bind=my_engine)
    db_session.bind = my_engine
    session = db_session()
    return session


def eng_sess(db_name):
    command = r'sqlite:///' + db_path(db_name)
    engine = create_engine(command)
    session = create_session(command)
    return command, engine, session




