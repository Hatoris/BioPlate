===========
Library usage
===========

>>> from BioPlate import BioPlate

>>> my_plate = BioPlate(12, 8)
>>>print(my_plate)
[[' ' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12']
 ['A' '' '' '' '' '' '' '' '' '' '' '' '']
 ['B' '' '' '' '' '' '' '' '' '' '' '' '']
 ['C' '' '' '' '' '' '' '' '' '' '' '' '']
 ['D' '' '' '' '' '' '' '' '' '' '' '' '']
 ['E' '' '' '' '' '' '' '' '' '' '' '' '']
 ['F' '' '' '' '' '' '' '' '' '' '' '' '']
 ['G' '' '' '' '' '' '' '' '' '' '' '' '']
 ['H' '' '' '' '' '' '' '' '' '' '' '' '']]
>>> value_of_wells = ["non_treated",  "control solvant", "conc1",  "conc2",  "conc3", "conc4", "conc5", "conc6",  "conc7", "media only"]
>>>my_plate.set("2-11[B-G]", value_of_wells)
>>> print(my_plate)
[[' ' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12']
 ['A' '' '' '' '' '' '' '' '' '' '' '' '']
 ['B' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['C' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['D' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['E' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['F' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['G' '' 'non_treated' 'control solvant' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['H' '' '' '' '' '' '' '' '' '' '' '' '']]

