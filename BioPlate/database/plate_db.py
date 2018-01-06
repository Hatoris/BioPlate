import BioPlate.database.database_function_import as dfi
from sqlalchemy import Column, Integer, String, Float


class PlateDB:

    database_name = 'plate.db'

    class PlateDatabase(dfi.Base):
        """
        Database for plate
        """

        __tablename__ = "plate"
        __table_args__ = {'useexisting': True}

        id = Column(Integer, primary_key=True)
        numWell = Column(Integer, nullable=False)
        numColumns = Column(Integer, nullable=False)
        numRows = Column(Integer, nullable=False)
        name = Column(String(250))
        surfWell = Column(Float)
        maxVolWell = Column(Float)
        workVolWell = Column(Float)
        refURL = Column(String(250))

        def __str__(self):
            if self.name:
                return f"<plate N°{self.id} :  {self.name} , {self.numWell}-{self.numColumns}-{self.numRows}>"
            else:
                return f"<plate N°{self.id} : {self.numWell}-{self.numColumns}-{self.numRows}>"

        def __repr__(self):
            if self.name:
                return f"<plate N°{self.id} :  {self.name} , {self.numWell}-{self.numColumns}-{self.numRows}>"
            else:
                return f"<plate N°{self.id} : {self.numWell}-{self.numColumns}-{self.numRows}>"

    @classmethod
    def from_database_name(cls, dbname):
        cls.database_name = dbname
        plate = cls(db_name=dbname)
        return plate

    def __init__(self, db_name = database_name):
        self.db_name = db_name
        self.sqlalchemypath, self.engine, self.session = dfi.eng_sess(self.db_name)
        self.table_create = dfi.create_table(self.sqlalchemypath)


    def add_plate(self, numWell, numColumns, numRows, name=None, surfWell=None, maxVolWell=None, workVolWell=None,
                  refURL=None):
        """
        add plate in the database
        :param session: Sqlalchemy session
        :param numWell: number of well in a plate (INT)
        :param numColumns:
        :param numRows:
        :param name:
        :param surfWell:
        :param maxVolWell:
        :param workVolWell:
        :param refURL:
        :return: Nothing
        """
        already_exist = self.session.query(self.PlateDatabase).filter_by(
                numWell = numWell,
                numColumns = numColumns,
                numRows=numRows,
                name=name,
                surfWell=surfWell,
                maxVolWell=maxVolWell,
                workVolWell=workVolWell,
                refURL=refURL).count()

        if not already_exist:
            new_entry = self.PlateDatabase(
                    numWell=numWell,
                    numColumns=numColumns,
                    numRows=numRows,
                    name=name,
                    surfWell=surfWell,
                    maxVolWell=maxVolWell,
                    workVolWell=workVolWell,
                    refURL=refURL)

            self.session.add(new_entry)
            self.session.commit()
            self.session.close()
            return f"plate with {numWell} added to the database"
        else:
            return None

    def get_plate(self, args, key='numWell'):
        """

        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        plt = self.session.query(self.PlateDatabase).filter(getattr(self.PlateDatabase, key) == args).all()
        self.session.close()
        return plt

    @property
    def get_all_plate(self):
        """
        get list of plate in the database
        :param session: Sqlalchemy session
        :param numWell: number of well in a plate (INT)
        :return: a list of plate object
        """
        all_plate = self.session.query(self.PlateDatabase).all()
        self.session.close()
        return all_plate

    def delete_plate(self, args, key='numWell'):
        """

        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        dplt = self.session.query(self.PlateDatabase).filter(getattr(self.PlateDatabase, key) == args).one()
        numwell = dplt.numWell
        self.session.delete(dplt)
        self.session.commit()
        self.session.close()
        return f"plate with {numwell} deleted"


if __name__ == '__main__':
    #PlateDB.from_database_name('plate2.db')
    pdb = PlateDB()
    #pdb = PlateDB.from_database_name('plate2.db')
    pdb.add_plate(numWell=96,
              numColumns=12,
              numRows=8,
              surfWell=0.29,
              maxVolWell=200,
              workVolWell=200,
              refURL='https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf')
    pdb.add_plate(numWell=6,
              numColumns=3,
              numRows=2,
              surfWell=9.5,
              maxVolWell=2000,
              workVolWell=2000,
              refURL='https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf')
    pdb.add_plate(numWell=24,
              numColumns=6,
              numRows=4,
              surfWell=0.33,
              maxVolWell=400,
              workVolWell=400,
              refURL='https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf')
    print(pdb.get_plate(96))
    p6 = pdb.get_plate(400, key='maxVolWell')
    print(p6)
    test = pdb.get_all_plate
    print(test)
