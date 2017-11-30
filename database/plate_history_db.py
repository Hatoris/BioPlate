from general_db import general_db
import marshal
import datetime

class plate_history_db(general_db):
        
    @property    
    @general_db.open_close(commit=True)
    def create_table(cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS plates_history (id INTEGER PRIMARY KEY AUTOINCREMENT, date TIMESTAMP, plateName TEXT, plate BLOB)")
     
    @general_db.open_close(commit=True)   	
    def save_plate(cursor, plateName, plate):
        value = (datetime.datetime.now(), plateName, marshal.dumps(plate)) 
        cursor.execute("INSERT INTO plates_history VALUES (Null,?,?,?) ", value) 

        
    @general_db.open_close(cursor=True)
    def get_by_plateName(cursor, plateName):
        cursor.execute('SELECT * FROM plates_history WHERE plateName=?', (plateName,)) 
        return cursor.fetchone() 
    
    @property
    @general_db.open_close(cursor=True)    
    def get_all(cursor):
        cursor.execute('SELECT * FROM plates_history')
        return cursor.fetchall()
        
    @general_db.open_close(commit=True)   
    def delete_by_id(cursor, id):
        cursor.execute('DELETE FROM plates_history WHERE id=?', (id,))
        
    @property
    @general_db.open_close(cursor=True)
    def get_column_name(cursor):
        curs = cursor.execute('SELECT * FROM plates_history WHERE id=0')
        names = [description[0] for description in curs.description]
        return names
    
        
    def get_dict(self, querys, key=False):
        names = self.get_column_name
        results = {}
        if isinstance(querys, list):
            for query in querys:
                if key == "plateName":
                    results[query[2]] = {}
                    dico = results[query[1]]
                else:
                    results[query[0]] = {}
                    dico = results[query[0]]
                for name, value in zip(names, query):
                    dico[name] = value
        elif isinstance(querys, tuple):
            for name, value in zip(names, querys):
                    if isinstance(value, bytes):
                        results[name] = marshal.loads(value)
                    else:
                        results[name] = value
        else:
            print("This is not a proper object : " + querys) 
        return results       
            
    def add_column_text(self, name):
        self.c.execute('ALTER TABLE plates ADD COLUMN ? TEXT', (name,)) 
        self.conn.commit()
        
if __name__ == "__main__":
    Plates = plate_history_db('plates_history.db')
    Plates.close
    #print(Plates.get_by_numWell(6))
    #Plates.delete_by_id(2)
    #print(Plates.get_all())
    #print(Plates.get_column_name)
    #Plates.add_column_text("refURL")
    #plate = Plates.get_dict(Plates.get_by_numWell(96))
    #print(plate['numWell'], plate['refURL']) 
    #print(Plates.get_by_numWell(24))
    All = Plates.get_all
    well = Plates.get_by_plateName('test1')
    print(All)
    print(well) 
    print(Plates.get_column_name)
    print(Plates.get_dict(well))
    #print(Plates.get_dict(Plates.get_by_numWell(24), key="numWell"))
    liat = [[0, 1, 2], ['A', 'B'], ['', ''], ['', '' ]]
    #Plates.save_plate('test1', liat) 
    data = marshal.dumps(liat, 4)
    Data = marshal.loads(All[0][3])
    print(Data[0])
    #print(data) 
        
        
    