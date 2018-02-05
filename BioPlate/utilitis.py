import functools
import time


#@functools.lru_cache(maxsize=None)
def dimension(plate):
	"""
	evaluate dimension of plate (2 or 3).
	plate : np.array
	return True if plate is a stack of 2D plate (=3D), false if plate object is only one plate and raise error if dimiaion is above 3.
	"""
	shape = plate.shape
	if len(shape) == 3:
		if shape[0] > 2:
			return True
		else:
			raise ValueError(f"plate object have a dimision of {shape[0]} > 3")
	else:
		return False
		
def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('%s function took %0.3f ms'%("test", (time2-time1)*1000.0))
        return ret
    return wrap
	
def dict_unique(dict_infos):
	n = 0
	for keys, values in dict_infos.items():
		if n == 0:
			save = values
			n = 1
		else:
			try:
				for key, value in values.items():
					in_save = save.get(key)
					if in_save:
						save[key] = in_save + value
					else:
						save[key] = value
			except AttributeError:
				return dict_infos
	return save