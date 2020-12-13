from src.main.python.entity.entity import Entity
from src.main.python.entity.item import Goods, Ore, Gas
from tools import set_attribute_for_all_elements


class Cargo(Entity):
	"""
	Class used to represent and manage cargo - a set of items.
	Cargo is created when two Entities interact (item transfer)
	"""
	attributes_dict = Entity.attributes_dict_copy()
	attributes_dict['item_dict'] = lambda x: isinstance(x, dict), dict()

	base_name = 'Cargo'

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			item_dict: dict(Item(cls), float)
		}
		"""

		self.item_dict: dict = None
		super().__init__(**kwargs)
		self.mass = sum(item.mass * qty for item, qty in self.item_dict.items())
		self.volume = sum(item.volume * qty for item, qty in self.item_dict.items())

	def __str__(self):
		items = '\n\t'.join([str(i) for i in self.item_dict.items()])
		return f"{self.obj_info}:\n\t{items}"

	def get_all_by_class(self, cls):
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return {k: v for k, v in self.item_dict.items() if issubclass(k.__class__, cls)}

	def get_total_mass_by_class(self, cls):
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return sum([k.mass * v for k, v in self.item_dict.items() if issubclass(k.__class__, cls)])

	def get_total_volume_by_class(self, cls):
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return sum([k.volume * v for k, v in self.item_dict.items() if issubclass(k.__class__, cls)])


class NotEnoughSpaceError(Exception):
	"""
	Exception raised when Cargo can not be stored to Storage since there is not enough space
	"""
	pass


class CanNotReserveCargoError(Exception):
	"""
	Exception raised when Cargo can not be reserved from Storage
	"""
	pass


class CargoNotExpectedError(Exception):
	"""
	Exception raised when Cargo tried to be stored without being expected in Storage
	"""
	pass


class Storage(Entity):
	"""
	Class used to represent and manage storage of Entity
	"""

	storage_types_tuple = (Goods, Ore, Gas)

	attributes_dict = Entity.attributes_dict_copy()
	attributes_dict['stored_items_list'] = lambda x: isinstance(x, list) and x[0] and issubclass(type(x[0]), list(Storage.storage_types_tuple)), list()
	attributes_dict['capacity'] = lambda x: isinstance(x, dict) and set(x.keys()) == set(Storage.storage_types_tuple) and bool(sum(x.values())), {Goods: 0.0, Ore: 0.0, Gas: 0.0}
	attributes_dict['reserved_cargo'] = lambda x: isinstance(x, list) and x[0] and isinstance(x[0], Cargo), list()
	attributes_dict['expected_cargo'] = lambda x: isinstance(x, list) and x[0] and isinstance(x[0], Cargo), list()

	base_name = 'Storage'

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			stored_items_list: list(Item),
			capacity: dict{Goods: float, Ore: float, Gas: float},
			reserved_cargo: list(Cargo),
			expected_cargo: list(Cargo)
		}
		"""

		self.stored_items_list = None
		self.capacity = None
		self.reserved_cargo = None
		self.expected_cargo = None

		super().__init__(**kwargs)

		set_attribute_for_all_elements(self.stored_items_list, 'parent_env', self)
		set_attribute_for_all_elements(self.reserved_cargo, 'parent_env', self)

	@property
	def obj_info(self):
		capacity = '; '.join([f'{k.__name__}: {v}' for k, v in self.capacity.items()])
		reserved_space = '; '.join([f'{t.__name__}: {self.get_reserved_space_by_class(t)}' for t in self.storage_types_tuple])
		filled_space = '; '.join([f'{t.__name__}: {self.get_filled_space_by_class(t)}' for t in self.storage_types_tuple])
		available_space = '; '.join([f'{t.__name__}: {self.get_available_space_by_class(t)}' for t in self.storage_types_tuple])
		items = '\n\t\t'.join([str(i) for i in self.stored_items_list])
		return f"{super().obj_info}:\n\tC=({capacity});\n\tRS=({reserved_space});\n\tOS=({filled_space});\n\tAS=({available_space});\n\t\t{items}"

	def __str__(self):
		return f"{self.obj_info_short}:"

	@property
	def total_mass(self):
		return sum([i.total_mass for i in self.stored_items_list])

	def get_reserved_space_by_class(self, cls):
		"""
		Returns total reserved space by incoming cargo by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return sum([c.get_total_volume_by_class(cls) for c in self.expected_cargo])

	def get_filled_space_by_class(self, cls):
		"""
		Returns total filled space by stored cargo by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return sum([i.total_volume for i in self.stored_items_list if issubclass(type(i), cls)])

	def get_occupied_space_by_class(self, cls):
		"""
		Returns sum of total filled space by stored cargo and total reserved space by incoming cargo by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return self.get_filled_space_by_class(cls) + self.get_reserved_space_by_class(cls)

	def get_available_space_by_class(self, cls):
		"""
		Returns value of available for use space by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return self.capacity[cls] - self.get_occupied_space_by_class(cls)

	def expect_cargo(self, cargo: Cargo):
		"""

		:param cargo: Cargo (an item set) to reserve space for
		:return: True if successful
		"""

		for cls in self.storage_types_tuple:
			if cargo.get_total_volume_by_class(cls) > self.get_available_space_by_class(cls):
				raise NotEnoughSpaceError(f"Can not reserve space for cargo since there's not enough space in {cls.__name__} storage!\n"
										  f"Available space: {self.get_available_space_by_class(cls)}\n"
										  f"Required space: {cargo.get_total_volume_by_class(cls)}")

		self.expected_cargo.append(cargo)

		return True

	def store(self, cargo: Cargo):
		"""

		:param cargo: Cargo (an item set) to store
		:return: True if successful
		"""

		# Check if cargo expected
		if cargo not in self.expected_cargo:
			raise CargoNotExpectedError("Can not store cargo since it was not expected!")

		# Store cargo
		for item in cargo.item_list:
			item.parent_env = self
			for i in range(len(self.stored_items_list) + 1):
				if i == len(self.stored_items_list):
					self.stored_items_list.append(item)
					break
				if type(self.stored_items_list[i]) == type(item):
					self.stored_items_list[i].quantity += item.quantity
					break

		# Free space
		self.expected_cargo.remove(cargo)

		# Delete cargo object
		self.delete(cargo)

		return True

	def reserve_cargo(self, cargo: Cargo):

		for item in cargo.item_list:
			pass
