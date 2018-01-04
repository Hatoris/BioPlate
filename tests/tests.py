import BioPlate.database.plate_db as pdb
import os

db_name = 'plate.db'
print(os.path.basename(os.getcwd()))
print(os.path.abspath('./database/DBFiles/plate.db'))
print(os.path.isfile(os.path.abspath(os.path.join(os.pardir, os.path.join('BioPlate/database/DBFiles', db_name)))))
print(os.path.isfile(os.path.abspath(os.path.join(os.pardir, os.path.join('BioPlate/database/DBFiles', db_name)))))
print(os.path.abspath(os.path.join(os.pardir, os.path.join('BioPlate/database/DBFiles', db_name))))