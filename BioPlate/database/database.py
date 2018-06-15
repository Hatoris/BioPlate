from pathlib import Path, PurePath

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, exc


class Database:

    Base = declarative_base()

    def __init__(self, database_class, db_name):
        self.db_name = db_name
        self.sqlalchemypath = self.create_sqlalchemypath
        self.engine = create_engine(self.sqlalchemypath)
        self.session = self.create_session
        self.table_create = self.create_table
        # specific to each database
        self.database_class = database_class

    @property
    def create_table(self):
        """
        This function is used to return a sqlalchemy session
    
        :param sqlalchemypath: 'sqlite:////./plate.db'
        :return: a sqlalchemy session object
        """

        my_engine = create_engine(self.sqlalchemypath)
        self.Base.metadata.create_all(my_engine)
        return f"{self.sqlalchemypath} table create"

    @property
    def create_session(self):
        """
        This function is used to return a sqlalchemy session
    
        :param sqlalchemypath: 'sqlite:////./plate.db'
        :return: a sqlalchemy session object
        """
        my_engine = create_engine(self.sqlalchemypath)
        self.Base.metadata.bind = my_engine
        db_session = sessionmaker(bind=my_engine)
        session = db_session()
        return session

    @property
    def create_sqlalchemypath(self):
        folder = Path(__file__).parent.absolute() / "DBFiles"
        folder.mkdir(parents=True, exist_ok=True)
        return r"sqlite:///" + str(PurePath(folder, self.db_name))

    def get_one(self, args, key=None):
        """
            def get_plate(self, args, key=' numWell'):
                super(PlateDB, self).get(args, key=key)
                
        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        try:
            if not key:
                raise ValueError("Get should have à default key! ")
            return (
                self.session.query(self.database_class)
                .filter(getattr(self.database_class, key) == args)
                .one()
            )
        except exc.MultipleResultsFound:
            self.session.rollback()
            return "Use a more specific key to get one object"
        finally:
            self.session.close()

    def get(self, **kwargs):
        """
            def get_plate(self, args, key=' numWell'):
                super(PlateDB, self).get(args, key=key)
                
        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        try:
            return self.session.query(self.database_class).filter_by(**kwargs).all()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_all(self):
        """
        get list of plate in the database
        :param session: Sqlalchemy session
        :param numWell: number of well in a plate (INT)
        :return: a list of plate object
        """
        try:
            return self.session.query(self.database_class).all()
        except Exception as e:
            self.session.rollback()
            return e
        finally:
            self.session.close()

    def delete(self, args, key=None):
        """

        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        try:
            if not key:
                raise ValueError("Delete should have à default key! ")
            dplt = (
                self.session.query(self.database_class)
                .filter(getattr(self.database_class, key) == args)
                .one()
            )
            self.session.delete(dplt)
            self.session.commit()
            return f"plate with {args} {key} deleted"
        except exc.MultipleResultsFound:
            self.session.rollback()
            return "Use a more specific key to delete the object"
        finally:
            self.session.close()

    def update(self, dict_update, args, key=None):
        """   dict_update = {"key to update" : new_value} """
        try:
            if not key:
                raise ValueError("Update should have à default key! ")
            obj = (
                self.session.query(self.database_class)
                .filter(getattr(self.database_class, key) == args)
                .one()
            )
            for keys, value in dict_update.items():
                setattr(obj, keys, value)
            self.session.commit()
            return f"plate with {args} {key} updated"
        except exc.MultipleResultsFound:
            self.session.rollback()
            return "Use a more specific key to update the object"
        finally:
            self.session.close()
