def set_attribute_for_all_elements(elem_list, attr_name, attr_val):
	for e in elem_list:
		e.__setattr__(attr_name, attr_val)