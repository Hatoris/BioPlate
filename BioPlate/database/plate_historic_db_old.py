import BioPlate.database.database_function_import as dfi
from sqlalchemy import Column, Integer, String, Date, PickleType
from BioPlate.plate import Plate
import datetime

class PlateHist:

    database_name = 'plate_historic.db'

    class PlateHistoric(dfi.Base):
        """
        historic of create plate
        """

        __tablename__ = "plate_historic"
        __table_args__ = {'useexisting': True}

        id = Column(Integer, primary_key=True)
        Plate_id = Column(Integer)
        numWell = Column(Integer, nullable=False)
        date = Column(Date, nullable=False)
        plate_name = Column(String(250), unique=True, nullable=False)
        plate_array = Column(PickleType, nullable=False)



        def __str__(self):
            if self.plate_name:
                return "<plate N°" + str(self.id) + ": " + self.plate_name + ", "+ str(self.numWell) + " wells, " + str(self.date)  + ">"
            else:
                return "<plate N°" + str(self.id) + ": " + str(self.numWell) + " wells, " + str(self.date)  + ">"

        def __repr__(self):
            if self.plate_name:
                return "<plate N°" + str(self.id) + ": " + self.plate_name + ", "+ str(self.numWell) + " wells, " + str(self.date) + ">"
            else:
                return "<plate N°" + str(self.id) + ": " + str(self.numWell) + " wells, " + str(self.date)  + ">"

    @classmethod
    def from_database_name(cls, dbname):
        cls.database_name = dbname
        plate = cls(db_name=dbname)
        return plate

    def __init__(self, db_name = database_name):
        self.db_name = db_name
        self.sqlalchemypath, self.engine, self.session = dfi.eng_sess(self.db_name)
        self.table_create = dfi.create_table(self.sqlalchemypath)

    def add_plate(self, numWell, plate_name, plate_array, Plate_id=None):
        """

        :param Plate_id: id of plate in plate.db
        :param numWell: int, number of well in plate
        :param date: date where plate was creating
        :param plate_name: name of experiment or plate
        :param plate_array: numpy array representation of the plate
        :return:
        """
        already_exist = self.session.query(self.PlateHistoric).filter_by(
                Plate_id = Plate_id,
                numWell = numWell,
                date=self.date_now,
                plate_name=plate_name,
                plate_array=plate_array).count()

        if not already_exist:
            new_entry = self.PlateHistoric(
                        Plate_id=Plate_id,
                        numWell=numWell,
                        date=self.date_now,
                        plate_name=plate_name,
                        plate_array=plate_array)

            self.session.add(new_entry)
            self.session.commit()
            self.session.close()
            return f"plate {plate_name} with {numWell}  added to the database"
        else:
            return None

    def get_plate(self, args, key='numWell'):
        """

        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        Plt = self.session.query(self.PlateHistoric).filter(getattr(self.PlateHistoric, key) == args).all()
        self.session.close()
        return Plt


    @property
    def get_all_plate(self):
        """
        get list of plate in the database
        :param session: Sqlalchemy session
        :param numWell: number of well in a plate (INT)
        :return: a list of plate object
        """
        all_plate = self.session.query(self.PlateHistoric).all()
        self.session.close()
        return all_plate

    def delete_plate(self, args, key='numWell'):
        """

        :param session: sqlalchemy session
        :param args: args to search of
        :param key: column name in the database
        :return:
        """
        dplt = self.session.query(self.PlateHistoric).filter(getattr(self.PlateHistoric, key) == args).one()
        numwell = dplt.numWell
        self.session.delete(dplt)
        self.session.commit()
        self.session.close()
        return f"plate with {numwell} deleted"

    @property
    def date_now(self):
        date = datetime.datetime.now()
        return datetime.date(date.year, date.month, date.day)

if __name__ == '__main__':
    v = {'A[2,8]': 'VC', 'H[2,8]': 'MS', '1-4[B,G]': ['MLR', 'NT', '1.1', '1.2'], 'E-G[8,10]': ['Val1', 'Val2', 'Val3']}
    plt = Plate(96)
    plt.add_values(v)

    w = {'A[1,3]' : 'Endo', 'B1' : 'Peri'}
    plt2 = Plate(6)
    plt2.add_values(w)

    ph = PlateHist()
    ph.add_plate(Plate_id = plt.plates.id,
                 numWell = plt.plates.numWell,
                 plate_name="First plate to test",
                 plate_array = plt.plate)
   
    ph.add_plate(Plate_id = plt2.plates.id,
                 numWell = plt2.plates.numWell,
                 plate_name="Second plate to test",
                 plate_array = plt2.plate)
    when = datetime.date(2018, 1, 7)
    p6 = ph.get_plate(when, key='date')[0]
    #p6 = ph.get_plate(2018, key='date')
    print(p6.date)
    test = ph.get_all_plate
    print(test)
