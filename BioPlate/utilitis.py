import functools


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
		

	