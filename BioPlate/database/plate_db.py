from sqlalchemy import Column, Integer, String, Float

from BioPlate.database.database import Database


class PlateDB(Database):
    class PlateDatabase(Database.Base):
        """
        Database for plate
        """

        __tablename__ = "plate"
        __table_args__ = {"useexisting": True}

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

    def __init__(self, db_name="plate.db"):
        super().__init__(self.PlateDatabase, db_name)

    def add_plate(
        self,
        numWell,
        numColumns,
        numRows,
        name=None,
        surfWell=None,
        maxVolWell=None,
        workVolWell=None,
        refURL=None,
    ):
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
        already_exist = (
            self.session.query(self.database_class)
            .filter_by(
                numWell=numWell,
                numColumns=numColumns,
                numRows=numRows,
                name=name,
                surfWell=surfWell,
                maxVolWell=maxVolWell,
                workVolWell=workVolWell,
                refURL=refURL,
            )
            .count()
        )

        if not already_exist:
            new_entry = self.database_class(
                numWell=numWell,
                numColumns=numColumns,
                numRows=numRows,
                name=name,
                surfWell=surfWell,
                maxVolWell=maxVolWell,
                workVolWell=workVolWell,
                refURL=refURL,
            )

            self.session.add(new_entry)
            self.session.commit()
            self.session.close()
            return f"plate with {numWell} added to the database"
        else:
            return None

    def update_plate(self, dict_update, args, key="numWell"):
        return super().update(dict_update, args, key=key)

    def delete_plate(self, args, key="numWell"):
        return super().delete(args, key=key)

    def get_one_plate(self, args, key="numWell"):
        return super().get_one(args, key=key)

    def get_plate(self, **kwargs):
        return super().get(**kwargs)

    def get_all_plate(self):
        return super().get_all()
