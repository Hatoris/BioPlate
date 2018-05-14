=============
From excel
=============

This class use `pyexcel_xlsx`_ in order to read from spreasheet plate informations.

.. _`pyexcel_xlsx`: http://pyexcel.readthedocs.io/en/latest/

Common use case
----------------------------------

This class is a simple way to transform a plate representation in a spreadsheet to a BioPlate instance.

An exemple
----------------------

>>> from BioPlate.writer.from_excel import BioPlateFromExcel
>>> inserts = BioPlateFromExcel(r"C:\Users\Florian\Desktop\my_inserts.xlsx", sheets=["plate_representation",])
>>> inserts["plate_representation"]


.. warning::

    By default BioPlateFromExcel will transform each plate representation in sheet to BioPlate object. If a sheet don't contain a plate this will
    stop the programm.


Plate infos
--------------

Information of plate in a spreadsheet without plate header should be pass like this :


.. code-block:: python

    {"sheetname" : { "row" : 9,
                     "column" : 12,
                     "stack" : True,
                     "type" : "BioPlate"}}
