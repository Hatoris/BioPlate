from typing import *


from BioPlate.core.matrix import BioPlateMatrix as bpm


class Index:
    
    CACHE = {}
   
    def __new__(cls, index, **kwargs):
       id_index = id(index)
       if id_index not in Index.CACHE:
           Index.CACHE[id_index] =  Index.serialize_index(index)
       return Index.CACHE[id_index]
   
    def serialize_index(index):
       if isinstance(index, (str)):
           return Index.index_str(index)
       elif isinstance(index, (tuple, list)):
           return Index._index_tuple_list(index)
       return index

    def _index_tuple_list(index):
        well = tuple()
        for i in index:
            digest = Index.serialize_index(i)
            if isinstance(digest, tuple):
                well += digest
            else:
                well += (digest,)
        return well

    def index_str(index):
        base = {"top" : 0, "bot" : 1}
        well = base.get(index, False)
        if well is not False:
            return well
        well = bpm(index)
        return (well.row, well.column)
       
    def is_string_in(index):
        if Index.is_string(index):
            return True
        elif isinstance(index, (tuple, list)):
            for ind in index:
                if Index.is_string(ind):
                    return True
                pass
        return False
       
    def is_string(index):
        return isinstance(index, str)