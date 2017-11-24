import sqlite3

conn = sqlite3.connect('plates.db')

class create_plate_db:

    def __init__(self, conn):
        self.c = conn.cursor()
      
    def create_table(self):
        self.c.execute("CREATE TABLE plates (id integer primary key autoincrement, numWell integer, numColumns integer, numRows integer, surfWell real)" 
    