=============
From excel
=============

This class use `pyexcel_xlsx`_ in order to read from spreasheet plate informations.

.. _`pyexcel_xlsx`: https://

Common use case
----------------------------------

This class is a simple way to transform plate representation in spreadsheet to a BioPlate instance.

An exemple
----------------------

>>> from BioPlate.writer.from_excel import BioPlateFromExcel
>>> inserts = BioPlateFromExcel(r"C:\Users\Florian\Desktop\my_inserts.xlsx")
>>>inserts