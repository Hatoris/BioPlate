===================
Set values on plate
===================

.. code:: python
    
    from BioPlate import BioPlate

On simple plate
--------------------------

.. code:: python

    simple_plate = BioPlate(12, 8)
    simple_plate.set("A1", "test1")


On inserts plate
----------------------------

.. code:: python

    inserts_plate = BioPlate(6, 4, inserts=True)
    inserts_plate.top.set("A1", "test1 on top")

.. note::
    
    Inserts plate are made of two parts, a *top* and a *bottom*. In order to assign value on an Inserts plate you should first select a part with `top` or `bot`.

On stack of plate
----------------------------

.. code:: python

    plate1 = BioPlate(12, 8)
    plate2 = BioPlate(12, 8)
    stack = plate1 + plate2
    stack.set(0, "A1", "test3 on plate1")
    print(plate1)

.. note::
    
    A stack is made of multiple plate, in order to select which plate you want to assign values, you should provide the plate index in stack as first arguments.


Set one value at time
-----------------------------------

.. code:: python

    plate = BioPlate(12, 8)
    plate.set("B1", "well B1")
    plate[1,2] = "well B2" #assign a well value with numpy indexing

Set value on column
----------------------------------

.. code:: python

    plate = BioPlate(12, 8)
    plate.set("3", "column 3")
    plate[1:,4] = "column 4" #assign a well value with numpy indexing
    plate.set("5[A-C]", "column 5")
    plate[1:4,6] = "column 6"

Set value on row
---------------------------

.. code:: python

    plate = BioPlate(12, 8)
    plate.set("B", "row B")
    plate[3,1:] = "row C" #assign a well value with numpy indexing
    plate.set("D[2-5]", "row D")
    plate[5,2:6] = "row E"

Set multiple value at once
----------------------------------------------

Assign multiple value with same patern:

.. code:: python    

    plate = BioPlate(12, 8)
    plate.set("2-4[A-G]", ["column2", "column3", "column4"]) # assign value in column
    plate.set("A-G[5-8]", ["rowA", "rowB", "rowC", "rowD", "rowE", "rowF", "rowG" ) #asign value in row

Assign multiple value with dict:

.. code:: python   

    plate = BioPlate(12, 8)
    plate.set({"A1" : "wellA1", "3[A-C]" : "column3", "E[4-7]" : "rowE", "6-8[E-G]" : ["column6", "column7", "column8"]})

Important
-------------------

.. warning::
     - If you use numpy indexing to assign be carrefull to not overide your header. Value are in position plate[1:,1:] where column header are on plate[0] and row header are on plate[0, 1:].
     - set method override, only the last assignation a well will be kept.