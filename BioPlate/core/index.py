from typing import *


from BioPlate.core.matrix import BioPlateMatrix as bpm


class Index:
    
    CACHE = {}
   
    def __new__(cls, index, **kwargs):
       try:
           id_index = hash(index)
       except TypeError:
           return Index.serialize_index(index)
       if id_index not in Index.CACHE:
           Index.CACHE[id_index] =  Index.serialize_index(index)
       return Index.CACHE[id_index]
   
    def serialize_index(index):
       if isinstance(index, (str)):
           return Index.index_str(index)
       elif isinstance(index, (tuple, list)):
           return Index._index_tuple_list(index)
       return None,  (index,)

    def _index_tuple_list(index):
        well = tuple()
        for i in index:
            try:
                pos, digest = Index.serialize_index(i)
            except TypeError:
                pos = None
                digest = Index.serialize_index(i)
            if isinstance(digest, tuple):
                well += digest
            else:
                well += (digest,)
        return pos, well

    def index_str(index):
        base = {"top" : 0, "bot" : 1, "TOP" : 0, "BOT" : 1}
        well = base.get(index, False)
        if well is not False:
            return well
        well = bpm(index)
        return well.pos, (well.row, well.column)
       
    def is_string_in(index):
        if Index.is_string(index):
            return True
        elif isinstance(index, (tuple, list)):
            for ind in index:
                if Index.is_string(ind):
                    return True
        return False
       
    def is_string(index):
        return isinstance(index, str)