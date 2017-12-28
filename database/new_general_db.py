from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base() 

class Plate(Base):

    """
    Database for plate 
    """
    
    __tablename__ = "plate" 
    
    id = Column(Integer, primary_key=True)
    numWell = Column(Integer, nullable=False)
    numColumns = Column(Integer, nullable=False) 
    numRows = Column(Integer, nullable=False)
    surfWell = Column(Float) 
    maxVolWell = Column(Float)
    workVolWell = Column(Float)
    refURL = Column(String(250))
    
    def __str__(self):
        return str(self.numWell) + "-" + str(self.numColumns) + "-" + str(self.numRows)
    
class Plate_Historic(Base):
    
    """
    historic of create plate
    """
    
    __tablename__ = 'Plate_Historic' 
    
    id = Column(Integer, primary_key=True)
    Plate_id = Column(Integer, ForeignKey('Plate.id'))
    numWell = Column(Integer)
    date = Column(DateTime)
    plate_name = Column(String(250))
    plate_sentence = Column(PickleType)
    plate_representation = Column(PickleType)
    

    
engine = create_engine('sqlite:////storage/emulated/0/qpython/projects3/BioPlate/database/plate.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession() 

def add_plate(session, numWell=None, numColumns=None, numRows=None, surfWell=None, maxVolWell=None, workVolWell=None, refURL=None):
     new_entry = Plate(numWell=numWell , numColumns=numColumns, numRows=numRows, surfWell=surfWell, maxVolWell=maxVolWell, workVolWell=workVolWell, refURL=refURL)
     session.add(new_entry)
     session.commit()
     
def get_plate(session, numWell):
    Plt = session.query(Plate).filter(Plate.numWell == numWell).one()
    return Plt
    
     
#add_plate(session, numWell=96,  numColumns=12, numRows=8, surfWell=0.29, maxVolWell=200, workVolWell=200, refURL='https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f') 
#add_plate(session, numWell=6,  numColumns=3, numRows=2, surfWell=9.5, maxVolWell=2000, workVolWell=2000, refURL=' https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f') 
#(6, 3, 2, 9.5, 2000, 2000,  ' https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f'))
#24, 6, 4, 0.33, 400, 400, 'https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f')
#add_plate(session, numWell=24, numColumns=6, numRows=4,  surfWell=0.33, maxVolWell=400, workVolWell=400, refURL='https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f') 


if __name__ == '__main__':

    plate1 = session.query(Plate).first() 
    print(plate1)
    print(plate1.numWell)
    all = session.query(Plate).all()
    #p6 = session.query(Plate).filter(Plate.numWell == 6).one()
    p6 = get_plate(session, 96)
    print("plate 6 : " + str(p6)) 
