=========
Database
==========


BioPlate use `sqlalchemy`_  in order to manipulate sqlite3 database.  Each database file are stock in the script under `BioPlate/database/DBfiles`.

.. _`sqlalchemy`: http://www.sqlalchemy.org


Common database method
-------------------------

Plate database and plate historic database bot inherit of database parent class.
Each function in commun should be call on an instance and by adding one of this suffix :

PlateDB : `_plate`
PlateHist : `_hplate`

Eg: For get method you will call it like that :

For PlateDB :

`self.get_plate()`

For PlateHist:

`self.get_hplate()`

eg :

`>>> plt = PlateDB()`<br>
`>>> plate_96 = plt.get_plate(96)`<br>
`>>> plate_96`<br>
`[<plate N°1 : 96-12-8>]`<br>
`>>> print(plate_96[0].name)`<br>
`None`<br>
`>>> print(plate_96[0].surfWell)`<br>
`0.29`<br>
`>>> update = {"name" : "plate_for_MTT_test", "surfWell" : 0.3}`<br>
`>>> plt.update_plate(update, 96)`<br>
`>>> plate_96_update = plt.get_plate(96)`<br>
`>>> plate_96_update.name`<br>
`plate_for_MTT_test`<br>
`>>> plate_96_update.surfWell`<br>
`0.3`<br>

Get one plate object
---------------------

`get(self, args, key="numWell")`


Get plate object matching given elements
-----------------------------------------

`get(self, **kwargs,")`

where `**kwargs` are pair of key, value you are looking for :

eg : `" numWell" = 96,  "surfWell"  = 0.29 `

This function return a list of object containing all element matching the query.

`PlateDB.get_plate(96)`<br>
`[<plate N°1 : 96-12-8>, <plate N°26 : cool name,  96-12-8>]`

If no result, retun an empty list

Get all elements in given database
-----------------------------------

`get_all(self)`

This function return all elements stock in the database object.


`[<plate N°1 : 96-12-8>,  <plate N°2 : cool 24 plate, 24-6-4>, < ... >, <plate N°26 : cool name,  96-12-8>] `

If database is empty, return an empty list

Update plate object in database
--------------------------------

`update(self, dict_update, args, key="numWell")`

where `dict_update` is a dictionary of key and value to update :

`{"key to update" : "New value"} `

eg : `{"name" : "plate_for_MTT_test", "surfWell" : 0.3}`

where `args` is value you are looking for :

eg : 96 for number of well

Where `key` is column name of data you looking for , by default `key` is numWell in both database.

**Be carefull `args` and `key` should be enought specific to return a unique match, is recomended to use `id` as `key`.**

This function return `f"plate with {args} {key} updated"`
OR
return `"Use a more specific key to update the object"`



Delete plate object in database
---------------------------------

`delete(self, args, key="numWell")`

where `args` is value you are looking for :

eg : 96 for number of well

Where `key` is column name of data you looking for , by default `key` is numWell in both database.

**Be carefull `args` and `key` should be enought specific to return a unique match, is recomended to use `id` as `key`.**


This function return `f"plate with {args} {key} deleted"`
OR
return `"Use a more specific key to delete the object"`