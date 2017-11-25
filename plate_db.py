import sqlite3
import sys



class create_plate_db:

    def __init__(self, DB):
        #try:
        self.DB = DB
        self.conn = self.connexion
        #except :
            #print(sys.exc_info()[0]) 
        self.c = self.conn.cursor()
        #self.close = self.conn.close()
      
    @property
    def close(self):
        return self.conn.close()
        
    @property
    def connexion(self):
        return sqlite3.connect(self.DB)
        
    @property
    def cursor(self):
        return self.conn.cursor()
        
    def open_close(connexion=False, cursor=False):
        def pass_func(func):
            def pass_self(self, func):
                def wrapper(self, *args, **kwargs):
                    conn = self.connexion
                    if connexion:
                        print("connexion")
                    elif cursor:
                        print("cursor")
                    else:
                        print("none of this") 
                    val = func(self, conn, *args) 
                    conn.close
                    print("close")
                    return val
                return wrapper
            return pass_self
        return pass_func

        
        
    
    def create_table(self):
        #self.conn
        self.c.execute("CREATE TABLE plates (id integer primary key autoincrement, numWell integer, numColumns integer, numRows integer, surfWell real, volWell real, workVol real, refURL text)")
        self.conn.commit()
        #self.close
        	
    def add_value(self, value):
        #self.conn
        self.c.execute("INSERT INTO plates VALUES (Null,?,?,?,?,?,?,?) ", value) 
        self.conn.commit()
        #self.close
        
    @open_close(cursor=True)
    def get_by_numWell(self, conn, numWell):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plates WHERE numWell=?', (numWell,)) 
        return cursor.fetchone() 
        
    def get_all(self):
        self.c.execute('SELECT * FROM plates')
        return self.c.fetchall()
        
    def delete_by_id(self, id):
        self.c.execute('DELETE FROM plates WHERE id=?', (id,))
        self.conn.commit()
        
    def get_column_name(self):
        cursor = self.c.execute('SELECT * FROM plates WHERE id=0')
        names = [description[0] for description in cursor.description]
        return names
        
    def get_dict(self, query):
        names = self.get_column_name()
        results = {} 
        for name, value in zip(names, query):
            results[name] = value
        return results
        
    def add_column_text(self, name):
        self.c.execute('ALTER TABLE plates ADD COLUMN ? TEXT', (name,)) 
        self.conn.commit()
        
if __name__ == "__main__":
    Plates = create_plate_db('/storage/emulated/0/qpython/projects3/BioPlate/plates.db')
    #Plates.create_table()
    #Plates.add_value((96, 12, 8, 0.29, 200, 200, 'https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f'))
    #Plates.add_value((6, 3, 2, 9.5, 2000, 2000,  ' https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f'))
    #print(Plates.get_by_numWell(6))
    #Plates.delete_by_id(2)
    #print(Plates.get_all())
    #print(Plates.get_column_name())
    #Plates.add_column_text("refURL")
    #plate = Plates.get_dict(Plates.get_by_numWell(96))
    #print(plate['numWell'], plate['refURL']) 
    Plates.close
    print(Plates.get_by_numWell(6))
    print(Plates.get_all())
        
        
        
    