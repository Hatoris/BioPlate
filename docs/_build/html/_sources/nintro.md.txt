Introduction
============

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

```python

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
from BioPlate.Plate import BioPlate

plt = BioPlate(96)
```

Or

```python

plt = BioPlate(12, 8)
```

Add values to your plate: 

In one well:

```python

plt.set("A1", "Control")
```

Or in multiple wells on a row: 

```

plt.set("C[2,10]", "Test1" )
```

Or in multiple wells on a column:

```

plt.set("11[B,G]", "Test2")
```

Or all in one 

```

Value = { "A1" : "Control", "C[2,10]" : "Test1", "11[B,G]" : "Test2"}

plt.set(value) 
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

```eval_rst
.. note:: Supported table formats to suply as key argument (eg: :code:`tablefmt="plain"`)

	.. hlist::
		:columns: 3
		
		* plain
		* simple
		* grid
		* fancy_grid
		* pipe
		* orgtbl
		* jira
		* presto
		* psql
		* rst
		* mediawiki
		* moinmoin
		* youtrack
		* html
		* latex
		* latex_raw
		* latex_booktabs
		* textile

```


# Advanced usage 

## Database

BioPlate use [SQLAlchemy](http://www.sqlalchemy.org) in order to manipulate sqlite3 database.  Each database file are stock in the script under `BioPlate/database/DBfiles`. 

### Commun database method
```eval_rst 

Plate database (:any:`PlateDB`) and plate historic (:any:`PlateHist`) database bot inherit of database parent class (:any:`Database`). 
Each function in commun should be call on an instance and by adding one of this suffix :
	
```

PlateDB : `_plate`
PlateHist : `_hplate`
```eval_rst

eg: For :any:`get` method you will call it like that :
```

For PlateDB : 

```
self.get_plate()
```

For PlateHist:

```
self.get_hplate()
```
 

#### get_one

```
get_one(self, args, key="numWell")
```

#### get 

```
get(self, **kwargs)
```

where `**kwargs` are pair of key, value you are looking for : 

eg : `" numWell" = 96,  "surfWell"  = 0.29 ` 

This function return a list of object containing all element matching the query. 

```eval_rst
.. code-block:: python

	>>> PlateDB.get_plate(96)
	[<plate N°1 : 96-12-8>, <plate N°26 : cool name,  96-12-8>]


If no result, retun an empty list ( :code:`[ ]` )
```


#### get_all

```
get_all(self)
```

This function return all elements stock in the database. 


```eval_rst
.. code-block:: python

	[<plate N°1 : 96-12-8>,  <plate N°2 : cool 24 plate, 24-6-4>, < ... >, <plate N°26 : cool name,  96-12-8>] 

If database is empty, return an empty list  ( :code:`[ ]` )
```

#### update 

```
update(self, dict_update, args, key="numWell")
```

where `dict_update` is a dictionary of key and value to update : 

`{"key to update" : "New value"} `

eg : `{"name" : "plate_for_MTT_test", "surfWell" : 0.3}`

where `args` is value you are looking for : 

eg : 96 for number of well 

Where `key` is column name of data you looking for , by default `key` is numWell in both database. 
```eval_rst
.. warning::
	
	Be carefull :code:`args` and :code:`key` should be enought specific to return a unique match, is recomended to use :code:`id` as :code:`key`.

```

This function return 

`"plate with {args} {key} updated"`

OR

`"Use a more specific key to update the object"`

eg :

```eval_rst

.. code-block:: python

	>>> plt = PlateDB()
	>>> plate_96 = plt.get_one_plate(96)
	>>> plate_96
	<plate N°1 : 96-12-8>
	>>> print(plate_96.name)
	None
	>>> print(plate_96.surfWell)
	0.29
	>>> update = {"name" : "plate_for_MTT_test", "surfWell" : 0.3}
	>>> plt.update_plate(update, 96)
	>>> plate_96_update = plt.get_one_plate(96)
	>>> plate_96_update.name
	plate_for_MTT_test
	>>> plate_96_update.surfWell
	0.3
```


#### delete

```
delete(self, args, key="numWell")

```

where `args` is value you are looking for : 

eg : 96 for number of well 

Where `key` is column name of data you looking for , by default `key` is numWell in both database. 

```eval_rst
.. warning::
	
	Be carefull :code:`args` and :code:`key` should be enought specific to return a unique match, is recomended to use :code:`id` as :code:`key`.

```


This function return 

`"plate with {args} {key} deleted"`

OR

`"Use a more specific key to delete the object"`  

# Futur version 

1. Implementation of  a comand line interface
2. Get volume and surface of each conditions 
3. Implementation of [pint](https://pint.readthedocs.io/en/latest/) to work directly with unit
6. Add Q-PCR protocol

# Version logs

## version 0.1.0

public realese 
