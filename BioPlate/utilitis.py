import functools
import time
import numpy as np

from string import ascii_uppercase
from pyexcel_xlsx import get_data


_LETTER = np.array(list(ascii_uppercase))


def dimension(plate):
    """
    evaluate dimension of plate (2 or 3).
   plate : np.array
    return True if plate is a stack of 2D plate (=3D), false if plate object is only one plate and raise error if dimiaion is above 3.
    """
    shape = plate.shape
    if len(shape) == 3:
        if shape[0] >= 2:
            return True
        else:
            raise ValueError(f"plate object have a dimision of {shape[0]} > 3")
    else:
        return False


def timing(f):
    """

    :param f:
    :return:
    """
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('%s function took %0.3f ms' % ("test", (time2 - time1) * 1000.0))
        return ret

    return wrap



def dict_unique(dict_infos):
    """

    :param dict_infos:
    :return:
    """
    unique = {}
    for keys, values in dict_infos.items():
    	try:
    		for key, value in values.items():
    			if key not in unique:
    				unique[key] = value
    			else:
    				unique[key] = unique[key] + value
    	except AttributeError:
    		return dict_infos
    return unique
    
def remove_empty_iterate(iterate, hd=None):
	dim = dimension(np.array(iterate))
	n = 0
	if dim:
		rm_empty = []
		for row in iterate:
			rm_empty +=  remove_empty(row)
			if not n and hd:
				rm_empty = hd + rm_empty
				n = 1
	else:
		rm_empty = remove_empty(iterate)
		if hd:
			rm_empty = hd + rm_empty
	return rm_empty
	
def remove_empty(iterate):
	rm_empty = []
	for row in iterate:
		rm_empty.append(list(filter(None, row)))
	return rm_empty
    	
def remove_tail(liste):
    lis = liste[::-1]
    for i, val in enumerate(lis):
        if not val:
            del lis[i]
            liste = lis[::-1]
            return remove_tail(liste)
        else:
             return liste   	
    	
def like_read_excel(plate, header=True, lst=None):
    rm_empty = [] if lst is None else lst
    if plate.name == "BioPlate":
            return clean_list(rm_empty, plate, header=header)
    elif plate.name == "BioPlateInserts":
        n = 0
        for parts in plate:
            parts= parts if header else parts[1:,1:]
            u = len(parts)
            for part in parts:
                if header:
                    if n == 0:
                        part[0] = "TOP"
                    elif u == n:
                        part[0] = "BOT"
                if u == n:
                     rm_empty.append([])                 
                clean_list(rm_empty, part, parts=True)
                n += 1
        return rm_empty

def like_read_excel_stack(stack, header=True):
    ll = None
    for plate in stack:
        if ll is None:
            ll = like_read_excel(plate, header=header, lst=None)
        else:
            ll = like_read_excel(plate, header=header, lst=ll)
        ll.append([])
    del ll[-1]
    return ll

def clean_list(li, plate, parts=False, header=True):
    if not parts:
        plate = plate if header else plate[1:,1:]
        for x in plate:
            li.append(remove_tail(list(x)))
    else:
        li.append(remove_tail(list(plate)))
    return li
 
def as_read_excel(PTE, action, plate, filename, sheetname, conditions=None):
    if conditions:
        for attr, value in conditions.items():
            setattr(PTE,  attr, value)
    getattr(PTE, action)(plate)
    getattr(PTE, 'close')()
    return get_data(filename)[sheetname]
  
def like_read_data(plate, accumulate=True, order="C", header=None, stack=False):
    rm_empty = list(map(list, getattr(plate, "iterate")(accumulate=accumulate, order=order)))
    if header is not None:
        pass
    else:
        val = len(rm_empty[0])
        if plate.name == "BioPlate":
            header = ['well', 'value0']
        elif plate.name == "BioPlateInserts":
            if accumulate:
                header = ["well", "top0", "bot0"]
            else:
                header = ["well", "top", "bot"]                            
        if val <= 2:
            pass
        else:
            if plate.name == "BioPlateInserts":
                pass
#                if val <= 3:
#                    for i in range(1, val):
#                        header.append('top' + str(i))
#                        header.append('bot' + str(i))
            elif plate.name == "BioPlate":
                for i in range(1, val):
                    header.append('value' + str(i))               
    if not stack:
        rm_empty.insert(0, header)
    return list(map(remove_tail, rm_empty))
   
def like_read_data_stack(stack, accumulate=True, order="C",  header=None):
    if stack[0].name == "BioPlate":
        if accumulate:
            header = ['well', 'value0']
        else:
            header = ['well', 'value']
    elif stack[0].name == "BioPlateInserts":
        if accumulate:
            header = ["well", "top0", "bot0"]
        else:
             header = ["well", "top", "bot"]
    if accumulate:
        for i in range(1, len(stack)):
            if stack[0].name == "BioPlateInserts":
                header.append('top' + str(i))
                header.append('bot' + str(i))
            else:
                header.append('value' + str(i))
    rm_empty = list(map(list, getattr(stack, "iterate")(accumulate=accumulate, order=order)))
    rm_empty.insert(0, header)
    return list(map(remove_tail, rm_empty))
   
def like_read_count(plate, empty="empty", Inserts=False):
    val = list(plate.count().items())
    if isinstance(val[0][1], dict):
        nv = []
        for pos, valdict in val:
           valdict = list(map(list, valdict.items()))
           addp = lambda x: [pos, ] + x
           nv += list(map(addp, valdict))
        val = nv
        if isinstance(val[0][2], dict):
            nv = []
            for i in range(len(val)):
                num, pos, valdict = val[i]
                valdict = list(map(list, valdict.items()))
                addp = lambda x: [num, pos ] + x
                nv += list(map(addp, valdict))
            val = nv
    val = list(map(list, val))
    change = lambda x: empty if x == '' else x
    val = list(map(lambda y: list(map(change, y)), val))
    len_header = len(val[0])
    if len_header == 2:
        hd = ["infos", "count"]
    elif len_header == 3:
        if not Inserts:
            hd = ["plate", "infos", "count"]
        else:
            hd = ["position", "infos", "count"]
    elif len_header == 4:
            hd = ["plate", "position", "infos", "count"]
    val.insert(0, hd)
    return val

def nested_dict_to_list(dd):
    local_list = []
    for key, value in dd.items():
        local_list.append(key)
        local_list.extend(nested_dict_to_list(value))
    return local_list