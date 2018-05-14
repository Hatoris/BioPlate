============
To excel
============

This function or class use `xlsxwriter`_ in order to past informations on excel files.

.. _`xlsxwriter` : http://http://xlsxwriter.readthedocs.io

Common use case
----------------------------------

This function or class have for only purpose to offer possibility to share results in format that many people used, spread sheet.

An exemple
----------------------

>>> from BioPlate import BioPlate
>>> plate = BioPlate(12, 8)
>>> plate.set("2-11[B-G]", ["control", "t1", "t2", 
                                            "t3", "t4", "t5", "t6", 
                                            "t7", "t9"])

The simple way is to call `to_excel` from plate object:

>>> plate.to_excel(r"C:\Users\Florian\Desktop\my_plate.xlsx")

If you want more control over informations past to excel you should use this module instead

>>> from BioPlate.writer.to_excel import BioPlateToExcel
>>> bpte = BioPlateToExcel(r"C:\Users\Florian\Desktop\my_plate.xlsx")
>>> bpte.representation(plate)
>>> bpte.data(plate)
>>> bpte.count(plate)
>>> bpte.close()

To excel plate representation
--------------------------------------------------

A plate representation is put on excel, by default sheetname on book is "plate_representation".


A representation can have an header or not, each plate representation are separated by one empty row.

.. figure:: /images/simple_plate.png
   :scale: 25 %
   :alt: representation of simple plate
   
   This is a simple plate put in excel 
   
In order to differentiate two plates versus one inserts a "TOP" or "BOT" is apply on position 0, 0.

.. figure:: /images/inserts.png
   :scale: 25 %
   :alt: representation of inserts plate
   
   This is a inserts plate put in excel


To excel plate data
--------------------------------

Data are an iteration of plate values, each value will be listed on a spreadsheet column with well position as index (A1, B1...).

.. note:: 

    accumulate (True or False)
        all value will refer to a single index
        
    order (R or C)
        iterate value by row or column
         
    This option is only avaliable when `data` is call from BioPlateToExcel module
      
    header
        list of header name
          
.. figure:: /images/inserts_data.png
   :scale: 25 %
   :alt: representation of inserts data
   
   This is what look like a inserts plate data put in excel

To excel count
-------------------------

Count give number of occurance in a plate. This is pretty usefull when you have informations on plate.

.. note::
  
    empty
        name given to empty value
       
.. figure:: /images/inserts_count.png
   :scale: 25 %
   :alt: representation of inserts counts
   
   This is what look like a inserts plate counts put in excel