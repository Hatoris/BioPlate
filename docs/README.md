BioPlate
======

A simple application to generate annotated plates used in biological experiments. 

# Table of content 

1. [Installation](#installation)
2. [Basic use](#basic-use)
3. [Advanced usage](#advanced-usage)
> 1. [Plate database](#plate-database)
> > 1. [Plate database object](#plate-database-object)
> > 2. [Add plate](#add-plate)
> > 3. [Delete plate](#delete-plate)
> 2. [Plate object](#plate-object)
4. [Futur version](#futur-version) 



# Installation 

`pip install BioPlate `

Or go on github.com :

`git clone`

# Basic use

First add your plate to database :

`from BioPlate.database.plate_db import PlateDB`

`pdb = PlateDB()`
`pdb.add_plate(numWell =96, numColumns = 12, numRows = 8, surfWell = 0.29, maxVolWell = 200, workVolWell = 200, refURL = useful.url.reference.com)`

with : 
* numWell : number of well in plate created
* numColumns : number of column in plate created
* numRows : number of row in plate created
* surfWell : surface of one well in cm^2
* maxVolWell : maximum volume avaliable in uL
* workVolWell : volume use in each well in uL


Then create your first plate object:

`from BioPlate.plate import Plate`

`plt = Plate(96)`

Or
 
`plt = Plate(12, key="numColumns")`

Add values to your plate: 

`plt.add_value("A1", "Control")`

Or

`plt.add_value_row("C[2,10]", "Test1" )`

Or

`plt.add_value_column("11[B,G]", "Test2")`

Or 

All in one 

`Value = { "A1" : "Control", "C[2,10]" : "Test1", "11[B,G]" : "Test2"}`

`plt.add_values(value) `

Then you can render your plate by using :

`plt.table(plt.plate)`

And here is the result in mardown :

(add mardown table) 

LaTeX:

(add LaTeX table)

and  all format you want using [tabulate](https://pypi.python.org/pypi/tabulate)  key arguments.

# Advanced usage 

## Plate database

BioPlate use [sqlalchemy](http://www.sqlalchemy.org) in order to manipulate sqlite3 database. 

### Plate database object



### Add plate 

### Delete plate

## Plate object 

# Futur version 

1. Implementation of  comand line interface
2. Ability to save plate in database historic
3. Get surface use following well used 
4. Get volume of each conditions 
5. Implementation of [pint](https://pint.readthedocs.io/en/latest/) to work directly with unit 

