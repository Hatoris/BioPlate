import sqlite3
import sys
import os
import re



class general_db:

    def __init__(self, DB):
        if re.search('database', sys.path[0]):
            self.DB = os.path.join(sys.path[0], DB)
        else :
            self.DB = os.path.join(sys.path[0], 'database/' + DB) 
        self.conn = self.connexion
        self.c = self.conn.cursor()
        self.create_table
      
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