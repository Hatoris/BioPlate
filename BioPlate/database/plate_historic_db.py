database = 'DBFiles/plate_historic.db'
session = create_session('sqlite:///' + database)


class Plate_Historic(Base):
    """
    historic of create plate
    """

    __tablename__ = 'plate_historic'

    id = Column(Integer, primary_key=True)
    Plate_id = Column(Integer)
    numWell = Column(Integer)
    date = Column(DateTime)
    plate_name = Column(String(250))
    plate_sentence = Column(PickleType)
    plate_representation = Column(PickleType)


    def __str__(self):
        if self.plate_name:
            return "<plate N°" + str(self.id) + ": " + self.plate_name + ", "+ str(self.numWell) + "-" + str(self.date)  + ">"
        else:
            return "<plate N°" + str(self.id) + ": " + str(self.numWell) + "-" + str(self.date)  + ">"

    def __repr__(self):
        if self.plate_name:
            return "<plate N°" + str(self.id) + ": " + self.plate_name + ", "+ str(self.numWell) + "-" + str(self.date) + ">"
        else:
            return "<plate N°" + str(self.id) + ": " + str(self.numWell) + "-" + str(self.date)  + ">"


def get_plate(args, key='numWell'):
    """

    :param session: sqlalchemy session
    :param args: args to search of
    :param key: column name in the database
    :return:
    """
    Plt = session.query(plate_historic).filter(getattr(plate_historic, key) == args).all()
    return Plt


def get_all_plate():
    """
    get list of plate in the database
    :param session: Sqlalchemy session
    :param numWell: number of well in a plate (INT)
    :return: a list of plate object
    """
    All_plate = session.query(plate_historic).all()
    return All_plate

create_session('sqlite:///' + database)


if __name__ == '__main__':