BigIntro
=======

A simple application to generate annotated plates used in biological experiments.

# Table of content 

1. [Installation](#installation)
2. [Basic use](#basic-use)
3. [Advanced usage](#advanced-usage)
> 1. [Database](#database)
> > 1. [Commun database method](#commun-database-method)
>>> 1. [Get one](#get_one)
>>> 2. [Get](#get)
>>> 3. [Get all](#get_all)
>>> 4. [Update](#update)
>>> 5. [Delete](#delete)
>> 2. [Plate database](#plate-database)
>>> 1. [Add plate](#add_plate)
>> 3. [Historic database](#historic-database)
>>> 1. [Add historic](#add_hplate)
> 2. [Plate](#plate)
>>> 1. [Create plate object](#create-plate-object) 
>>> 2. [Add value in one well](#add-value-in-one-well) 
>>> 3. [Add value on a row](#add-value-on-a-row) 
>>> 4. [Add value on a column](#add-value-on-a-column) 
>>> 5. [Add multiple values in once](#add-multiple-values-in-once)
>>> 6. [Evaluate](#evaluate-expression)
>>> 6.  [Show table representation](#show-table-representation) 
>>> 7. [Save plate](#save-plate) 
4. [Futur version](#futur-version)
5. [Version logs](#version-logs) 



# Installation 

with pipy :

```bash
pip install BioPlate 
```

Or go on github.com :

```bash
git clone
```

# Basic use

First add your plate to database :

```

from BioPlate.database.plate_db import PlateDB

pdb = PlateDB()
pdb.add_plate(
    numWell =96,
    numColumns = 12,
    numRows = 8,
    surfWell = 0.29,
    maxVolWell = 200,
    workVolWell = 200,
    refURL = 'useful.url.reference.com'
    )
```

``` eval_rst
.. note::

        numWell : 
            number of well in plate created

        numColumns :
            number of column in plate created

        numRows :
            number of row in plate created

        surfWell : 
            surface of one well (eg : in :math:`cm^2`)

        maxVolWell :
            maximum volume avaliable (eg : in :math:`\mu{L}`)

        workVolWell :
            volume use in each well (eg: in :math:`\mu{L}`)

```

Then create your first plate object:

```python
from BioPlate.plate import Plate

plt = Plate(96)
```

Or

```python

plt = Plate(12, key="numColumns")
```

Add values to your plate: 

In one well:

```python

plt.add_value("A1", "Control")
```

Or in multiple wells on a row: 

```

plt.add_value_row("C[2,10]", "Test1" )
```

Or in multiple wells on a column:

```

plt.add_value_column("11[B,G]", "Test2")
```

Or all in one 

```

Value = { "A1" : "Control", "C[2,10]" : "Test1", "11[B,G]" : "Test2"}

plt.add_values(value) 
```

Then you can render your plate by using :

```
plt.table(plt.plate, stralign="center", tablefmt="rst")
```

Giving the following result in reStructeredText:

``` eval_rst
.. include:: table1.rst


```
```eval_rst
.. _tabulate: https://pypi.python.org/pypi/tabulate

.. important::
	
	 Table method use tabulate_ package. You can uses all its key arguments to format and render plate table !

```

# Advanced usage 

## Database

BioPlate use [sqlalchemy](http://www.sqlalchemy.org) in order to manipulate sqlite3 database.  Each database file are stock in the script under `database/DBfiles`. 

### Commun database method

Plate database and plate historic database bot inherit of database parent class. 
Each function in commun should be call on an instance and by adding one of this suffix :

PlateDB : `_plate`
PlateHist : `_hplate`

Eg: For get method you will call it like that :

For PlateDB : 

`self.get_plate()`

For PlateHist:

`self.get_hplate()`
 

#### get_one

`get(self, args, key="numWell")`

#### get 

`get(self, **kwargs,")`

where `**kwargs` are pair of key, value you are looking for : 

eg : `" numWell" = 96,  "surfWell"  = 0.29 ` 

This function return a list of object containing all element matching the query. 

`PlateDB.get_plate(96)`<br>
`[<plate N°1 : 96-12-8>, <plate N°26 : cool name,  96-12-8>]`

If no result, retun an empty list

#### get_all

`get_all(self)`

This function return all elements stock in the database object. 


`[<plate N°1 : 96-12-8>,  <plate N°2 : cool 24 plate, 24-6-4>, < ... >, <plate N°26 : cool name,  96-12-8>] `

If database is empty, return an empty list

#### update 

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



#### delete

`delete(self, args, key="numWell")`

where `args` is value you are looking for : 

eg : 96 for number of well 

Where `key` is column name of data you looking for , by default `key` is numWell in both database. 

**Be carefull `args` and `key` should be enought specific to return a unique match, is recomended to use `id` as `key`.**


This function return `f"plate with {args} {key} deleted"`
OR
return `"Use a more specific key to delete the object"`

### Plate database

#### add_plate

### Historic database

#### add_hplate

## Plate

### Create plate object

### Add value in one well

### Add value on a row

### Add value on a column

### Add multiple values in once

### Show table representation

### Save plate  


# Futur version 

1. Implementation of  a comand line interface
2. Get volume and surface of each conditions 
3. Implementation of [pint](https://pint.readthedocs.io/en/latest/) to work directly with unit
4. Get an excel file with plate representation 
5. Get in excel volume and surface informations for each conditions 
6. Add Q-PCR protocol

# Version logs

