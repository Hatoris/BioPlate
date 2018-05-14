===================
Set values on plate
===================

Set's function is used to quickly assign values to a plate.

Set on simple plate
---------------------------------

.. code:: python

     from BioPlate import BioPlate
     simple_plate = BioPlate(12, 8)
     simple_plate.set("A1", "test1")


Seton inserts plate
----------------------------------

.. code:: python

     from BioPlate import BioPlate
     inserts_plate = BioPlate(6, 4, inserts=True)
     
     #assign value on top of inserts plate
     inserts_plate.top.set("A1", "test1 on top")

.. note::
    
    Inserts plate are made of two parts, a *top* and a *bottom*. In order to assign value on an Inserts plate you should first select a part with attribute `top` or `bot`.

Set on stack of plate
------------------------------------

.. code:: python

     from BioPlate import BioPlate
     plate1 = BioPlate(12, 8)
     plate2 = BioPlate(12, 8)
     
     #create a stack of plate
     stack = plate1 + plate2
     
     #assign value to plate1
     stack.set(0, "A1", "test3 on plate1")

.. note::
    
    A stack is made of multiple plate, in order to select which plate you want to assign values, you should provide the plate index in stack as first arguments.


Set one value at time
-----------------------------------

.. code:: python

    from BioPlate import BioPlate
    plate = BioPlate(12, 8)
    
    #assign a well value
    
    #with set
    plate.set("B1", "well B1")
        
    #with numpy indexing
    plate[1,2] = "well B2" 

Set value on column
----------------------------------

.. code:: python

    from BioPlate import BioPlate
    plate = BioPlate(12, 8)
    
    #asign value on a column
    
    #with set
    plate.set("3", "column 3")
    plate.set("5[A-C]", "column 5")
        
    #with numpy indexing
    plate[1:,4] = "column 4"     
    plate[1:4,6] = "column 6"

Set value on row
---------------------------

.. code:: python

    from BioPlate import BioPlate
    plate = BioPlate(12, 8)
    
    #assign value on a row
    
    # with set
    plate.set("B", "row B")
    plate.set("D[2-5]", "row D")
    
    #with numpy indexing
    plate[3,1:] = "row C"
    plate[5,2:6] = "row E"

Set multiple value at once
----------------------------------------------

Assign multiple value with same pattern:

.. code:: python    

    from BioPlate import BioPlate
    plate = BioPlate(12, 8)
    
    # assign value in column
    plate.set("2-4[A-G]",
    ["column2", "column3", "column4"])
                     
     #asign value in row                
    plate.set("A-G[5-8]",
    ["rowA", "rowB", "rowC", 
    "rowD", "rowE", "rowF", "rowG"])

Assign multiple value with different pattern:

.. code:: python   

    from BioPlate import BioPlate   
    plate = BioPlate(12, 8)
    plate.set({
        "A1" : "wellA1",          
        "3[A-C]" : "column3", 
        "E[4-7]" : "rowE",         
        "6-8[E-G]" : ["column6", "column7", "column8"]})

Important
-------------------

.. hint::
    
    This is the higher level of indexing
   
    .. code::
        
        {"5-8[A-C]" : ["col5", "col6", "col7", "col8"]}
    
    and it is equivalent to:
    
    .. code::
        
        {"5[A-C]" : "col5", 
         "6[A-C]" : "col6", 
         "7[A-C]" : "col7", 
         "8[A-C]" : "col8"}
    
    which is finally equivalent to:
    
    .. code::
        
        {"A5" : "col5", "B5" : "col5", "C5" : "col5", 
         "A6" : "col6", "B6" : "col6", "C6" : "col6", 
         "A7" : "col7", "B7" : "col7", "C7" : "col7", 
         "A8" : "col8", "B8" : "col8", "C8" : "col8"}
    
    This is the lower level of indexing

.. warning::
     - If you use numpy indexing to assign be carrefull to not overide your header. Value are in position plate[1:,1:] where column header are on plate[0] and row header are on plate[0, 1:].
     - Set function keep only the last assignation of a value in a  well.