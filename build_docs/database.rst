================
Database options
================

BioPlate use `sqlalchemy`_  in order to manipulate sqlite3 database.  Each database file are stock in the script under `BioPlate/database/DBfiles`.

.. _`sqlalchemy`: http://www.sqlalchemy.org


Common database method
----------------------------------------------

Plate database and plate historic database bot inherit of database parent class.
Each function in commun should be call on an instance and by adding one of this suffix :

PlateDB : **`_plate`**

PlateHist : **`_hplate`**

Eg: For `get` method you will call it like that :

For PlateDB :

>>> from BioPlate.database.plate_db import PlateDB
>>> pdb = PlateDB()
>>> pdb.get_plate(96)

For PlateHist:

>>> from BioPlate.database.plate_historic_db import PlateHist
>>> ph = PlateHist()
>>> plate = ph.get_one_hplate("my Experiment 1", key="plate_name").plate_array

An exemple
----------------------

>>> from BioPlate.database.plate_db import PlateDB
>>> pdb= PlateDB()
>>> pdb.add_plate( numWell =96,
       numColumns = 12,
       numRows = 8,
       surfWell = 0.29,
       maxVolWell = 200,
       workVolWell = 200,
       refURL = 'useful.url.reference.com')
>>> plate_96 = pdb.get_one_plate(96)
>>> plate_96
<plate N°1 : 96-12-8>
>>> plate_96.name
 None
>>> plate_96.surfWell
0.29
>>> update = {"name" : "plate_for_MTT_test", "surfWell" : 0.3}
>>> pdb.update_plate(update, 96)
>>> plate_96_update = pdb.get_one_plate(96)
>>> plate_96_update.name
plate_for_MTT_test
>>> plate_96_update.surfWell
0.3

Use case of PlateDB and PlateHist
-----------------------------------------------------------

Both of this database can be used to save informations, on general plate informations (PlateDB) or on a users defined plate (PlateHist).

PlateDB
^^^^^^^^^^

This database will be used when always working with same plate format. This database are attended to be used to keep following informations :
    
.. note::
    
    numWell :
        number of well in plate created

    numColumns :
        number of column in plate created

    numRows :
        number of row in plate created

    surfWell :
        surface of one well 
        (eg : in :math:`cm^2`)

    maxVolWell :
        maximum volume avaliable 
        (eg : in :math:`\mu{L}`)

    workVolWell :
        volume use in each well
        (eg: in :math:`\mu{L}`)
        
    refURL :
        An url reference
        
PlateHist
^^^^^^^^^^

This database will be used to save plate filed with value. This database is attended to be used to keep following informations :
    
.. note::
    
    Plate_id :
        id of plate in PlateDB

    numWell :
        number of well in plate

    date :
        date when plate is added to the database

    plate_name :
        name of the given plate 
        (eg : "my expwriment 1")

    plate_array :
         plate object

Get one plate object
-------------------------------------

>>> from BioPlate.database.plate_db import PlateDB
>>> pdb = PlateDB()
>>> pdb.get_one_plate(args, key="numWell")


Get plate object matching given elements
----------------------------------------------------------------------

>>> from BioPlate.database.plate_db import PlateDB
>>> pdb = PlateDB()
>>> pdb.get_plate(self, **kwargs)

where `**kwargs` are pair of key, value you are looking for :

eg : `" numWell" = 96,  "surfWell"  = 0.29 `

This function return a list of object containing all element matching the query.

>>> pdb.get_plate(96)
>>> [<plate N°1 : 96-12-8>, <plate N°26 : cool name,  96-12-8>]

If no result, `get` retun an empty list.

Get all elements in given database
------------------------------------------------------------

>>> from BioPlate.database.plate_db import PlateDB
>>> pdb = PlateDB()
>>> pdb.get_all_plate()

This function return all elements stock in the database object.

>>> pdb.get_all_plate()
>>> [<plate N°1 : 96-12-8>,  <plate N°2 : cool 24 plate, 24-6-4>, < ... >, <plate N°26 : cool name,  96-12-8>] 

If database is empty, `get_all` return an empty list.

Update plate object in database
-------------------------------------------------------

>>> from BioPlate.database.plate_db import PlateDB
>>> pdb = PlateDB()
>>> pdb.update_plate(self, dict_update, args, key="numWell")

where `dict_update` is a dictionary of key and value to update :

eg : `{"name" : "plate_for_MTT_test", "surfWell" : 0.3}`

where `args` is value you are looking for :

eg : 96 for number of well

Where `key` is column name of data you looking for , by default `key` is numWell in both database.

.. warning::
    
    Be carefull **`args`** and **`key`** should be enought specific to return a unique match, is recomended to use **`id`** as **`key`**.

This function return `f"plate with {args} {key} updated"`
OR
return `"Use a more specific key to update the object"`


Delete plate object in database
------------------------------------------------------

>>> from BioPlate.database.plate_db import PlateDB
>>> pdb = PlateDB()
>>> pdb.delete_plate(args, key="numWell")`

where `args` is value you are looking for :

eg : `96, key="numWell"`

Where `key` is column name of data you looking for , by default `key` is numWell in both database.

.. warning::
    
    Be carefull **`args`** and **`key`** should be enought specific to return a unique match, is recomended to use **`id`** as **`key`**.


This function return `f"plate with {args} {key} deleted"`
OR
return `"Use a more specific key to delete the object"`