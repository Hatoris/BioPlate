import functools
import time
import numpy as np


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
    	
    	
    	
