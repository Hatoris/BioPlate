===================
Get values on plate
===================

Get's function is used to easily retrieve values from a plate.

.. hint::
    
    Get return a unique value if call for one well or it will return a `numpy.ndarray`_ for multiple well, to get a list you can use `.tolist()`_ .
    
.. _`numpy.ndarray`: https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.ndarray.html

.. _`.tolist()`: https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.ndarray.tolist.html

For demonstration purposes we will used following instances of plate objects.

.. code:: python
    
    from BioPlate import BioPlate
    plate = BioPlate(12, 8)
    plate1 = BioPlate(12, 8)
    inserts = BioPlate(12, 8, inserts=True)
    stack = plate + plate1
    stacki = BioPlate(3, 12, 8, inserts=True)
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
    stacki.set(0, "top", "6[D-E]", "insertsTop1")
    

Get on simple plate
--------------------------

.. code:: python

   A1 = plate.get("A1")
   B1 = plate["B1"]
   column = plate.get("3[A-C]")
   column1 = plate["4[A-C]"]
   row = plate.get("B-D[8-12]")
   row1 = plate["B-D[8-12]"]
   

Get on inserts plate
----------------------------------

.. code:: python

   A1_top_inserts = inserts.top.get("A1")
   B1_top_inserts = inserts["top", "B1"] #[0, "B1"]
   column_bot_inserts = inserts.bot.get("6[D-E]")
   column1_bot_inserts = inserts["bot", "7[D-E]"] # [1, "7[D-E]"]
   row_top_inserts = inserts.top.get("B-D[8-12]")
   row1_top_inserts = inserts[0, "B-D[4-8]"]

.. note::
    
    Inserts plate are made of two parts, a *top* and a *bottom*. In order to assign value on an Inserts plate you should first select a part with attribute `top` or `bot`.
        
Get on stack of plate
-----------------------------------

.. code:: python

    # For stack made of plate
    A1_plate1_stack = stack.get(0, "A1")
    B1_plate1_stack = stack[0, "B1"]
    column_plate2_stack = stack.get(1, "6[D-E]")
    column1_plate2_stack = stack[1, "6[D-E]"]
    row_plate1_stack = stack.get(0, "B-D[8-12]")
    
    # For stack made of inserts
    A1_inserts1_top_stack = stack.get(0, "top",  "A1")
    B1_inserts1_bot_stack = stack[0, 1, "B1"]
    column_inserts2_top_stack = stack.get(1, 0, "6[D-E]")
    column1_inserts2_bot_stack = stack[1, "bot", "6[D-E]"]
    row_inserts3_top_stack = stack.get(0, 0, "B-D[8-12]")
    
.. note::
    
    A stack is made of multiple plate, in order to select which plate you want to assign values, you should provide the plate index in stack as first arguments.


Get one value at time
-----------------------------------

.. code:: python

    A1 = plate.get("A1")
    A1_np = plate[1,1]
    A1_bp = plate["A1"]
    any(A1 == A1_np) # True
    any(A1_bp == A1_np) # True

Get value on column
----------------------------------

.. code:: python

    Column3 = plate.get("3")
    Column3_np = plate[1:,3]
    Column3_bp = plate["3"]
    any(Column3 == Column3_np)  # True
    any(Column3_bp == Column3_np)  # True
    
    Column5 = plate.get("5[A-C]")
    Column5_np = plate[1:4,5]
    Column5_bp = plate["5[A-C]"]
    any(Column5 == Column5_np) # True
    any(Column5_bp == Column5_np) # True
    
.. note::
    
    If you use bioplate indexation, column number should be pass as string, otherwise index will be interpreted as numpy index.

Get value on row
---------------------------

.. code:: python

    RowB = plate.get("B")
    RowB_np = plate[2,1:] 
    RowB_bp = plate["B"]
    any(RowB == RowB_np) # True
    any(RowB_bp == RowB_np) # True
    
    RowD = plate.get("D[2-5]")
    RowD_np = plate[4,2:6]
    RowD_bp = plate["D[2-5]"]
    any(RowD == RowD_np) # True
    any(RowD_bp == RowD_np) # True

Get multiple value at once
---------------------------------------------

This will return a numpy array.

.. code:: python    

    multiC = plate.get("2-4[A-G]")
    multiC_np = plate[1:8,2:5]
    multiC_bp = plate["2-4[A-C]"]
    (multiC == multiC_np).any() # True
    (multiC_bp == multiC_np).any() # True
    
    multiR = plate.get("A-G[5-8]")
    multiR_np = plate[1:8,5:9]
    multiR_bp = plate["A-G[5-8]"]
    (multiR == multiR_np).any() # True
    (multiR_bp == multiR_np).any() # True

This will return a list

.. code:: python

    multiAll = plate.get("A2", "B[2-6]", "H12")