from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

Base = declarative_base()


def db_path(db_name):
    """

    :param db_name: String, name of the db file
    :return: abspath of database in function of calling directory
    """
    path_to_database = {"BioPlate" : rf"{os.path.abspath(os.path.join('database/DBFiles', db_name))}",
                        "database" : rf"{os.path.abspath(os.path.join('DBFiles', db_name))}",
                        "tests" :  rf"{os.path.abspath(os.path.join(os.pardir, os.path.join('BioPlate/database/DBFiles', db_name)))}"}
    try:
        folder = os.path.basename(os.getcwd())
        return path_to_database[folder]
    except KeyError:
        return f"{folder} not in path to database"


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
    session = db_session()
    return session


def create_sqlalchemypath(db_name):
    return r'sqlite:///' + db_path(db_name)


def eng_sess(db_name):
    sqlalchemypath = create_sqlalchemypath(db_name)
    engine = create_engine(sqlalchemypath)
    session = create_session(sqlalchemypath)
    return sqlalchemypath, engine, session




