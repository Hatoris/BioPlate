=========
Exemples
=========

Context
--------------

You have a `MTT test`_ to performed. And all your protocole are writen in markdown. Moreover, you like pandas but your boss want to see your results in excel too. 

. . _`MTT test`: http://docutils.sourceforge.net/docs/user/rst/quickref.html



Create a rapid representation of a 96 well plate for an experiment
------------------------------------------------------------------------------------------------------------


>>> from BioPlate.plate import BioPlate
>>> my_plate = BioPlate(12, 8)
>>> infos = {2 : "non_treated", 3 : "control solvant", 4 : "conc1",  5 : "conc2", 6 : "conc3", 7 : "conc4", 8: "conc5", 9 : "conc6", 10 : "conc7", 11 : "media only"}
>>> my_plate.set(infos)
>>> print(my_plate)
[[' ' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12']
 ['A' '' '' '' '' '' '' '' '' '' '' '' '']
 ['B' '' 'non_treated' 'control solvan' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['C' '' 'non_treated' 'control solvan' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['D' '' 'non_treated' 'control solvan' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['E' '' 'non_treated' 'control solvan' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['F' '' 'non_treated' 'control solvan' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['G' '' 'non_treated' 'control solvan' 'conc1' 'conc2' 'conc3' 'conc4' 'conc5' 'conc6' 'conc7' 'media only' '']
 ['H' '' '' '' '' '' '' '' '' '' '' '' '']]
 
 Then you want to output your plate for paste it in your markdown file.
 
>>>my_plate.table()
     1    2            3               4      5      6      7      8      9      10     11          12
---  ---  -----------  --------------  -----  -----  -----  -----  -----  -----  -----  ----------  ----
A
B         non_treated  control solvan  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
C         non_treated  control solvan  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
D         non_treated  control solvan  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
E         non_treated  control solvan  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
F         non_treated  control solvan  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
G         non_treated  control solvan  conc1  conc2  conc3  conc4  conc5  conc6  conc7  media only
H

know your trainee want to get plate representation but in excel

>>>my_plate.to_excel("for_you_my_dear_trainee.xlsx")