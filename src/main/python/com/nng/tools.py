from math import pi


e_mass_kg = 5.97 * (10 ** 24)
e_volume_km3 = 1.08321 * (10 ** 12)
e_density_kg_per_sm3 = 5.51 / 1000


def set_attribute_for_all_elements(elem_list, attr_name, attr_val):
	for e in elem_list:
		e.__setattr__(attr_name, attr_val)


def calc_radius(mass, volume):
	"""
	Return radius in kilometers
	:param mass: relative to Earth's mass
	:param density: relative to Earth's density
	:return: radius - sphere's radius in kilometers
	"""
	# V = 4/3 * pi * r**3
	# r ** 3 = V / (4/3 * pi)
	# r = (V / (4/3 * pi)) ** (1/3)
	# V = mass / density
	# r = (mass / density / (4/3 * pi)) ** (1/3)
	return round(((volume * e_volume_km3) / (4/3 * pi)) ** (1/3), 4)
