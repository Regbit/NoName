from src.main.python.entity.entity import Entity
from src.main.python.entity.item import Item, Goods, Ore, Gas


class CargoSubtractionError(Exception):
	pass


class Cargo(Entity):
	"""
	Class used to represent and manage cargo - a set of items.
	Cargo is created when two Entities interact (item transfer)
	"""
	attributes_dict = Entity.attributes_dict_copy()
	attributes_dict['item_dict'] = lambda x: isinstance(x, dict) and len(x), dict()
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

	def __str__(self):
		items = '\n\t'.join([str(k.cls_name()) + f"; Q={v}" for k, v in self.item_dict.items()])
		return f"{self.obj_info}" + (f":\n\t{items}" if len(self.item_dict) else "")

	def __add__(self, other):
		new_item_dict = dict()
		for k in list(self.item_dict.keys()) + list(other.item_dict.keys()):
			new_item_dict[k] = (self.item_dict.get(k) or 0) + (other.item_dict.get(k) or 0)
		return Cargo(item_dict=new_item_dict)

	def __iadd__(self, other):
		new_item_dict = dict()
		for k in list(self.item_dict.keys()) + list(other.item_dict.keys()):
			new_item_dict[k] = (self.item_dict.get(k) or 0) + (other.item_dict.get(k) or 0)
		self.item_dict.update(new_item_dict)
		return self

	def __sub__(self, other):
		for k in other.item_dict.keys():
			if k not in self.item_dict:
				raise CargoSubtractionError(f"Cargo {self} does not have item {k} to subtract from!")
			elif self.item_dict[k] < other.item_dict[k]:
				raise CargoSubtractionError(f"Cargo {self} does not have {other.item_dict[k]} units of item {k} to subtract from!")

		new_item_dict = dict()
		for k in self.item_dict.keys():
			diff = self.item_dict.get(k) - (other.item_dict.get(k) or 0)
			if diff:
				new_item_dict[k] = diff

		return Cargo(item_dict=new_item_dict)

	def __isub__(self, other):
		for k in other.item_dict.keys():
			if k not in self.item_dict:
				raise CargoSubtractionError(f"Cargo {self} does not have item {k} to subtract from!")
			elif self.item_dict[k] < other.item_dict[k]:
				raise CargoSubtractionError(f"Cargo {self} does not have {other.item_dict[k]} units of item {k} to subtract from!")

		new_item_dict = dict()
		for k in self.item_dict.keys():
			diff = self.item_dict.get(k) - (other.item_dict.get(k) or 0)
			if diff:
				new_item_dict[k] = diff
		self.item_dict.update(new_item_dict)

		return self

	@property
	def mass(self) -> float:
		return sum(item.mass * qty for item, qty in self.item_dict.items())

	@property
	def volume(self) -> float:
		return sum(item.volume * qty for item, qty in self.item_dict.items())

	@property
	def is_empty(self) -> bool:
		return not bool(len(self.item_dict))

	def has_item(self, item_class) -> bool:
		return item_class in self.item_dict

	def get_all_by_class(self, cls) -> dict:
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return {k: v for k, v in self.item_dict.items() if issubclass(k, cls)}

	def get_total_mass_by_class(self, cls) -> float:
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return sum([k.mass * v for k, v in self.item_dict.items() if issubclass(k, cls)])

	def get_total_volume_by_class(self, cls) -> float:
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return sum([k.volume * v for k, v in self.item_dict.items() if issubclass(k, cls)])

	def update(self):
		pass


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
	attributes_dict['capacity'] = lambda x: isinstance(x, dict) and set(x.keys()) == set(Storage.storage_types_tuple) and bool(sum(x.values())), {Goods: 0.0, Ore: 0.0, Gas: 0.0}
	attributes_dict['stored_cargo'] = lambda x: x != x, Cargo()
	attributes_dict['reserved_cargo_list'] = lambda x: x != x, list()
	attributes_dict['expected_cargo_list'] = lambda x: x != x, list()

	base_name = 'Storage'

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			capacity: dict{Goods: float, Ore: float, Gas: float}
		}
		"""

		self.capacity: dict = None
		self.stored_cargo: Cargo = None
		self.reserved_cargo_list: list = None
		self.expected_cargo_list: list = None

		for attr in ('stored_cargo', 'reserved_cargo_list', 'expected_cargo_list'):
			if attr in kwargs:
				kwargs.pop(attr)

		super().__init__(**kwargs)

		self.stored_cargo.parent_env = self

	@property
	def obj_info(self) -> str:
		capacity = '; '.join([f'{k.__name__}: {v}' for k, v in self.capacity.items()])
		reserved_space = '; '.join([f'{t.__name__}: {self.get_reserved_space_by_class(t)}' for t in self.storage_types_tuple])
		filled_space = '; '.join([f'{t.__name__}: {self.get_filled_space_by_class(t)}' for t in self.storage_types_tuple])
		available_space = '; '.join([f'{t.__name__}: {self.get_available_space_by_class(t)}' for t in self.storage_types_tuple])
		items = '\n\t\t'.join([str(i) + f"({q})" for i, q in self.stored_cargo.item_dict.items()])
		return f"{super().obj_info}:\n\tC=({capacity});\n\tRS=({reserved_space});\n\tOS=({filled_space});\n\tAS=({available_space});\n\t\t{items}"

	def __str__(self):
		return f"{self.obj_info_short}:"

	@property
	def is_empty(self) -> bool:
		return self.stored_cargo.is_empty

	@property
	def total_stored_mass(self) -> float:
		return self.stored_cargo.mass

	@property
	def total_stored_volume(self) -> float:
		return self.stored_cargo.volume

	@property
	def available_cargo(self) -> Cargo:
		return self.stored_cargo - sum(self.reserved_cargo_list)

	def get_filled_space_by_class(self, cls) -> float:
		"""
		Returns total filled space by stored cargo by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return self.stored_cargo.get_total_volume_by_class(cls)

	def get_reserved_space_by_class(self, cls) -> float:
		"""
		Returns total reserved space by incoming cargo by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return sum([c.get_total_volume_by_class(cls) for c in self.expected_cargo_list])

	def get_occupied_space_by_class(self, cls) -> float:
		"""
		Returns sum of total filled space by stored cargo and total reserved space by incoming cargo by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return self.get_filled_space_by_class(cls) + self.get_reserved_space_by_class(cls)

	def get_available_space_by_class(self, cls) -> float:
		"""
		Returns value of available for use space by class
		:param cls: Goods, Ore or Gas
		:return: float
		"""
		return self.capacity[cls] - self.get_occupied_space_by_class(cls)

	def expect_cargo(self, cargo: Cargo) -> bool:
		"""
		Attempts to add Cargo to expected_cargo_list for space reservation.
		If there is not enough available space method raises NotEnoughSpaceError.
		:param cargo: Cargo (an item set) to reserve space for
		:return: True if successful
		"""

		for cls in self.storage_types_tuple:
			if cargo.get_total_volume_by_class(cls) > self.get_available_space_by_class(cls):
				raise NotEnoughSpaceError(f"Can not reserve space for cargo since there's not enough space in {cls.__name__} storage!\n"
										  f"Available space: {self.get_available_space_by_class(cls)}\n"
										  f"Required space: {cargo.get_total_volume_by_class(cls)}")

		self.expected_cargo_list.append(cargo)

		return True

	def store_cargo(self, cargo: Cargo) -> bool:
		"""
		Attempts to store Cargo.
		If Cargo was not expected (not in expected_cargo_list) then method raises CargoNotExpectedError.
		:param cargo: Cargo (an item set) to store
		:return: True if successful
		"""

		# Check if cargo expected
		if cargo not in self.expected_cargo_list:
			raise CargoNotExpectedError("Can not store cargo since it was not expected!")

		# Store cargo
		self.stored_cargo += cargo

		# Free space
		self.expected_cargo_list.remove(cargo)

		# Delete cargo object
		self.delete(cargo)

		return True

	def reserve_cargo(self, cargo: Cargo):

		for item in cargo.item_list:
			pass
