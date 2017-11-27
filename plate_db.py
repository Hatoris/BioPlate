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
        
    def open_close(connexion=False, cursor=False, commit=False):
        def pass_self(func):
            def wrapper(self, *args, **kwargs):
                conn = self.connexion
                curs = conn.cursor()
                if connexion:
                    val = func(conn, *args)
                elif cursor:
                    val = func(curs, *args)
                elif commit:
                    val = func(curs, *args)
                    conn.commit() 
                else:
                    print("none of this") 
                conn.close
                return val
            return wrapper
        return pass_self

        
    @property    
    @open_close(commit=True)
    def create_table(cursor):
        cursor.execute("CREATE TABLE plates (id integer primary key autoincrement, numWell integer, numColumns integer, numRows integer, surfWell real, volWell real, workVol real, refURL text)")
     
    @open_close(commit=True)   	
    def add_value(cursor, value):
        cursor.execute("INSERT INTO plates VALUES (Null,?,?,?,?,?,?,?) ", value) 

        
    @open_close(cursor=True)
    def get_by_numWell(cursor, numWell):
        cursor.execute('SELECT * FROM plates WHERE numWell=?', (numWell,)) 
        return cursor.fetchone() 
    
    @property
    @open_close(cursor=True)    
    def get_all(cursor):
        cursor.execute('SELECT * FROM plates')
        return cursor.fetchall()
        
    @open_close(commit=True)   
    def delete_by_id(cursor, id):
        cursor.execute('DELETE FROM plates WHERE id=?', (id,))
        
    @property
    @open_close(cursor=True)
    def get_column_name(cursor):
        curs = cursor.execute('SELECT * FROM plates WHERE id=0')
        names = [description[0] for description in curs.description]
        return names
    
        
    def get_dict(self, querys, key=False):
        names = self.get_column_name
        results = {}
        for query in querys:
            if key == "numWell":
                results[query[1]] = {}
                dico = results[query[1]]
            else:
                results[query[0]] = {}
                dico = results[query[0]]
            for name, value in zip(names, query):
                dico[name] = value
        return results
        
    def add_column_text(self, name):
        self.c.execute('ALTER TABLE plates ADD COLUMN ? TEXT', (name,)) 
        self.conn.commit()
        
if __name__ == "__main__":
    Plates = create_plate_db('/storage/emulated/0/qpython/projects3/BioPlate/plates.db')
    Plates.close
    #Plates.create_table()
    #Plates.add_value((96, 12, 8, 0.29, 200, 200, 'https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f'))
    #Plates.add_value((6, 3, 2, 9.5, 2000, 2000,  ' https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f'))
    #Plates.add_value((24, 6, 4, 0.33, 400, 400, 'https://www.google.ca/url?sa=t&source=web&rct=j&url=http://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf&ved=0ahUKEwiEueSp8tnXAhXySd8KHd_ECXgQFgg1MAA&usg=AOvVaw2X9oIuhZs3izCw7OmvQE_f'))
    #print(Plates.get_by_numWell(6))
    #Plates.delete_by_id(2)
    #print(Plates.get_all())
    #print(Plates.get_column_name())
    #Plates.add_column_text("refURL")
    #plate = Plates.get_dict(Plates.get_by_numWell(96))
    #print(plate['numWell'], plate['refURL']) 
    #print(Plates.get_by_numWell(24))
    All = Plates.get_all
    #print(All)
    #print(Plates.get_column_name)
    #print(Plates.get_dict(All, key="numWell"))
    print(Plates.get_dict(Plates.get_by_numWell(24), key="numWell"))
        
        
        
    