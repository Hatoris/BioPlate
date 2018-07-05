import datetime

from sqlalchemy import Column, Integer, String, Date, PickleType
from sqlalchemy.ext.hybrid import hybrid_property

import BioPlate
from BioPlate.database.database import Database


class PlateHist(Database):
    class PlateHistoric(Database.Base):
        """
        historic of create plate
        """

        __tablename__ = "plate_historic"
        __table_args__ = {"useexisting": True}

        id = Column(Integer, primary_key=True)
        Plate_id = Column(Integer)
        numWell = Column(Integer, nullable=False)
        date = Column(Date, nullable=False)
        plate_name = Column(String(250), unique=True, nullable=False)
        plate_array = Column(PickleType, nullable=False)

        @hybrid_property
        def plate(self):
            if isinstance(self.plate_array, list):
                return BioPlate.stack.Stack(self.plate_array)
            else:
                return self.plate_array

        def __str__(self):
            return (
                "<plate N°"
                + str(self.id)
                + ": "
                + self.plate_name
                + ", "
                + str(self.numWell)
                + " wells, "
                + str(self.date)
                + ">"
            )

        def __repr__(self):
            return (
                "<plate N°"
                + str(self.id)
                + ": "
                + self.plate_name
                + ", "
                + str(self.numWell)
                + " wells, "
                + str(self.date)
                + ">"
            )

    def __init__(self, db_name="plate_historic.db"):
        self.db_name = db_name
        super().__init__(self.PlateHistoric, db_name)

    def add_hplate(self, numWell, plate_name, plate_array, Plate_id=None):
        """

        :param Plate_id: id of plate in plate.db
        :param numWell: int, number of well in plate
        :param date: date where plate was creating
        :param plate_name: name of experiment or plate
        :param plate_array: numpy array representation of the plate
        :return:
        """
        already_exist = self.session.query(self.database_class).filter_by(
            Plate_id=Plate_id,
            numWell=numWell,
            date=self.date_now,
            plate_name=plate_name,
        )

        if not already_exist.count():
            new_entry = self.database_class(
                Plate_id=Plate_id,
                numWell=numWell,
                date=self.date_now,
                plate_name=plate_name,
                plate_array=plate_array,
            )

            self.session.add(new_entry)
            self.session.commit()
            self.session.close()
            Type = type(plate_array).__name__
            Type = "Stack" if Type == "list" else Type
            return f"{Type} {plate_name} with {numWell} wells was successfully added to database {self.db_name}"
        else:
            return already_exist[0].id

    def update_hplate(self, dict_update, args, key="numWell"):
        return super().update(dict_update, args, key=key)

    def delete_hplate(self, args, key="numWell"):
        return super().delete(args, key=key)

    def get_one_hplate(self, args, key="numWell"):
        return super().get_one(args, key=key)

    def get_hplate(self, **kwargs):
        return super().get(**kwargs)

    def get_all_hplate(self):
        return super().get_all()

    @property
    def date_now(self):
        date = datetime.datetime.now()
        return datetime.date(date.year, date.month, date.day)
