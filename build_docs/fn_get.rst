===================
Get values on plate
===================

Get's function is used to easily retrieve values from a plate.

.. hint::
    
    Get return a unique value if call for one well or it will return a `numpy.ndarray`_ for multiple well, to get list you can use `.tolist()`_ .
    
.. _`numpy.ndarray`: https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.ndarray.html

.. _`.tolist()`: https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.ndarray.tolist.html

For demonstration purposes we will used following instances of plate objects.

.. code:: python
    
    from BioPlate import BioPlate
    plate = BioPlate(12, 8)
    plate1 = BioPlate(12, 8)
    inserts = BioPlate(12, 8, inserts=True)
    stack = plate + plate1   
    value = {
       "A1" : "wellA1",
       "3[A-C]" : "column3", 
       "E[4-7]" : "row E", 
       "6-8[E-G]" : ["column6", "column7", "column8"], 
       "2[B-G]" : "column2", 
       "B-D[8-12]" : ["rowB", "rowC", "rowD"]
    }
    plate.set(value)
    inserts.top.set(value)
    inserts.bot.set("6[D-E]", "bottom")
    stack.set(1, "6[D-E]", "plate1")
    

Get on simple plate
--------------------------

.. code:: python

   A1 = plate.get("A1")
   column = plate.get("3[A-C]")
   row = plate.get("B-D[8-12]")
   

Get on inserts plate
----------------------------------

.. code:: python

   A1_top_inserts = inserts.top.get("A1")
   column_bot_inserts = inserts.bot.get("6[D-E]")
   row_top_inserts = inserts.top.get("B-D[8-12]")

.. note::
    
    Inserts plate are made of two parts, a *top* and a *bottom*. In order to assign value on an Inserts plate you should first select a part with `top` or `bot`.
        
Get on stack of plate
-----------------------------------

.. code:: python

    A1_plate_stack = stack.get(0, "A1")
    column_bot_inserts = inserts.bot.get("6[D-E]")
    row_top_inserts = inserts.top.get("B-D[8-12]")

.. note::
    
    A stack is made of multiple plate, in order to select which plate you want to assign values, you should provide the plate index in stack as first arguments.


Get one value at time
-----------------------------------

.. code:: python

    A1 = plate.get("A1")
    A1_np = plate[1,1]
    any(A1 == A1_np) # True

Get value on column
----------------------------------

.. code:: python

    Column3 = plate.get("3")
    Column3_np = plate[1:,3]
    any(Column3 == Column3_np)  # True
    
    Column5 = plate.get("5[A-C]")
    Column5_np = plate[1:4,5]
    any(Column5 == Column5_np) # True

Get value on row
---------------------------

.. code:: python

    RowB = plate.get("B")
    RowB_np = plate[2,1:] 
    any(RowB == RowB_np) # True
    
    RowD = plate.get("D[2-5]")
    RowD_np = plate[4,2:6]
    any(RowD == RowD_np) # True

Get multiple value at once
---------------------------------------------

.. code:: python    

    multiC = plate.get("2-4[A-G]")
    multiC_np = plate[1:8,2:5]
    (multiC == multiC_np).any() # True
    
    multiR = plate.get("A-G[5-8]")
    multiR_np = plate[1:8,5:9]
    (multiR == multiR_np).any() # True

