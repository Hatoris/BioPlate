import sqlite3
import sys



class create_plate_db:

    def __init__(self, DB):
        #try:
        self.conn = sqlite3.connect(DB)
        #except :
            #print(sys.exc_info()[0]) 
        self.c = self.conn.cursor()
        #self.close = self.conn.close()
      
    @property
    def close(self):
        return self.conn.close()
    
    def create_table(self):
        #self.conn
        self.c.execute("CREATE TABLE plates (id integer primary key autoincrement, numWell integer, numColumns integer, numRows integer, surfWell real, volWell real, workVol real)")
        self.conn.commit()
        #self.close
        	
    def add_value(self, value):
        #self.conn
        self.c.execute("INSERT INTO plates VALUES (Null,?,?,?,?,?,?) ", value) 
        self.conn.commit()
        #self.close
        
    def get_value(self, val):
        #self.conn
        #print(val) 
        r = self.c.execute('SELECT * FROM plates WHERE numWell=?', (96, )) 
        return self.c.fetchone()
        #print(self.c.fetchone())
        #self.close()
        
        
if __name__ == "__main__":
    Plates = create_plate_db('/storage/emulated/0/qpython/projects3/BioPlate/plates.db')
    #Plates.create_table()
    #Plates.add_value((96, 12, 8, 0.29, 200, 200))
    print(Plates.get_value(96)) 
    Plates.close
    
        
        
        
    