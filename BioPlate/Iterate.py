import numpy as np


class BioPlateIterate:
    """A row is symbolise by it's letter, a column by a number"""    
      
    def __new__(cls, plate, order="C", accumulate=True, OnlyValue=False):
        Order = {"C" : "F", "R" : "C"}
        cls.order = Order[order]
        cls.plate = plate
        cls.accumulate = accumulate
        cls.OnlyValue = OnlyValue
        if cls.OnlyValue:
            return cls._iterate()
        return cls.iterate()
        
    @classmethod        
    def iterate(cls):
        """
        generator return [well, value]
        
        :param plate: numpy.array of plate object
        :param order: iterate by column C or by row R
        """
        
        if cls.accumulate:
            row, column, values = cls._acumul_iterate()
            for r, c, *v in np.nditer((row, column) + values, order=cls.order):
                yield (cls._merge_R_C_(r, c),) + tuple(map(str, v))
        else:
            for row, column, value  in cls._iterate():
                for r, c, v in np.nditer((row, column, value), order=cls.order):
                    yield (cls._merge_R_C_(r, c), str(v))

         
    @classmethod   
    def _acumul_iterate(cls):
        values = []
        for row, column, value  in cls._iterate():
             values.append(value)
        return row, column, tuple(values)
    

    @classmethod                  
    def _iterate(cls):
        bps =  cls.plate.name == "BioPlateStack"
        bpi = cls.plate.name == "BioPlateInserts"
        bp = cls.plate.name == "BioPlate"
        if bp:
            yield from cls.__iterate(cls.plate)
        else:
            for pl in cls.plate:
                yield from cls.__iterate(pl)

    @classmethod                                          
    def __iterate(cls, plate):
            columns = plate[0,1:]
            rows = plate[1:, 0:1]
            values = plate[1:, 1:]
            if cls.OnlyValue:
                yield values
            else:
                yield rows, columns, values

    @classmethod      
    def _merge_R_C_(cls, row, column):
      RC =   "".join(map(str, [row, column]))
      return RC    

   

