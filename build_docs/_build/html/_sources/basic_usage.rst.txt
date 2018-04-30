=============
Library usage
=============

>>> from BioPlate import BioPlate

>>> my_plate = BioPlate(12, 8)
>>> print(my_plate)
[[' ' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12']
 ['A' '' '' '' '' '' '' '' '' '' '' '' '']
 ['B' '' '' '' '' '' '' '' '' '' '' '' '']
 ['C' '' '' '' '' '' '' '' '' '' '' '' '']
 ['D' '' '' '' '' '' '' '' '' '' '' '' '']
 ['E' '' '' '' '' '' '' '' '' '' '' '' '']
 ['F' '' '' '' '' '' '' '' '' '' '' '' '']
 ['G' '' '' '' '' '' '' '' '' '' '' '' '']
 ['H' '' '' '' '' '' '' '' '' '' '' '' '']]

Add values to well, here from column 2 to column 11 on row B to G. For more possibilities on how to set value go there.

>>> value_of_wells = ["non_treated",  "control solvant", "conc1",  "conc2",  "conc3", "conc4", "conc5", "conc6",  "conc7", "media only"]
>>> my_plate.set("2-11[B-G]", value_of_wells)
[[' ' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12']
 ['A' '' '' '' '' '' '' '' '' '' '' '' '']
 ['B' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['C' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['D' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['E' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['F' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['G' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['H' '' '' '' '' '' '' '' '' '' '' '' '']]


You can get a nice representation of your plate by calling `table` on it.

>>> print(my_plate.table())
     1    2            3                4      5      6      7      8      9      10     11          12
---  ---  -----------  ---------------  -----  -----  -----  -----  -----  -----  -----  ----------  ----
A
B         non_treated  control solvant  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
C         non_treated  control solvant  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
D         non_treated  control solvant  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
E         non_treated  control solvant  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
F         non_treated  control solvant  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
G         non_treated  control solvant  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
H
>>> print(my_plate.table(tablefmt="grid"))
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
|     | 1   | 2           | 3               | 4     | 5     | 6     | 7     | 8     | 9     | 10    | 11         | 12   |
+=====+=====+=============+=================+=======+=======+=======+=======+=======+=======+=======+============+======+
| A   |     |             |                 |       |       |       |       |       |       |       |            |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
| B   |     | non_treated | control solvant | conc1 | conc2 | conc3 | conc4 | conc5 | conc6 | conc7 | media only |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
| C   |     | non_treated | control solvant | conc1 | conc2 | conc3 | conc4 | conc5 | conc6 | conc7 | media only |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
| D   |     | non_treated | control solvant | conc1 | conc2 | conc3 | conc4 | conc5 | conc6 | conc7 | media only |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
| E   |     | non_treated | control solvant | conc1 | conc2 | conc3 | conc4 | conc5 | conc6 | conc7 | media only |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
| F   |     | non_treated | control solvant | conc1 | conc2 | conc3 | conc4 | conc5 | conc6 | conc7 | media only |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
| G   |     | non_treated | control solvant | conc1 | conc2 | conc3 | conc4 | conc5 | conc6 | conc7 | media only |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+
| H   |     |             |                 |       |       |       |       |       |       |       |            |      |
+-----+-----+-------------+-----------------+-------+-------+-------+-------+-------+-------+-------+------------+------+

We can also send a representation of plate in excel file.

>>> my_plate.to_excel(r"C:\Users\Florian\Desktop\my_plate.xlsx")