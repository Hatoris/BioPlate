from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc
import os



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
    def db_path(self):
        """
    
        :param db_name: String, name of the db file
        :return: abspath of database in function of calling directory
        """
        path_to_database = {"BioPlate": rf"{os.path.abspath(os.path.join('database/DBFiles', self.db_name))}",
                            "database": rf"{os.path.abspath(os.path.join('DBFiles', self.db_name))}",
                            "tests": rf"{os.path.abspath(os.path.join(os.pardir, os.path.join('BioPlate/database/DBFiles', self.db_name)))}"}
        try:
            folder = os.path.basename(os.getcwd())
            return path_to_database[folder]
        except KeyError:
            return f"{folder} not in path to database"
    
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
        return r'sqlite:///' + self.db_path
        
    def get(self, args, key=None):
        """
            def get_plate(self, args, key=' numWell'):
                super(PlateDB, self).get(args, key=key)
                
        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        if not key: 
            raise ValueError("Get should have à défaut key! ")
        plt = self.session.query(self.database_class).filter(getattr(self.database_class, key) == args).all()
        self.session.close()
        return plt
        
    def get_all(self):
        """
        get list of plate in the database
        :param session: Sqlalchemy session
        :param numWell: number of well in a plate (INT)
        :return: a list of plate object
        """
        all = self.session.query(self.database_class).all()
        self.session.close()
        return all
        
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
            dplt = self.session.query(self.database_class).filter(getattr(self.database_class, key) == args).one()
            self.session.delete(dplt)
            self.session.commit()
            self.session.close()
            return f"plate with {args} {key} deleted"
        except exc.SQLAlchemyError:
            return "Use a more specific key to delete the object"
            
    def update(self, dict_update, args, key=None):
        """   dict_update = {"key to update" : new_value} """
        try:
            if not key:
                raise ValueError("Delete should have à default key! ")
            self.session.query(self.database_class).filter(getattr(self.database_class, key) == args).one().update(dict_update)
            self.session.commit()
            self.session.close()
            return f"plate with {args} {key} updated" 
        except exc.SQLAlchemyError:
            return "Use a more specific key to delete the object"
            
            
    
    
    
