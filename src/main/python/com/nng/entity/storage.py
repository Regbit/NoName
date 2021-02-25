from com.nng.entity.entity import Entity
from com.nng.entity.item import Goods, Ore, Gas
from com.nng.entity.cargo import CargoSubtractionError, Cargo
from copy import deepcopy


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


class CanNotReleaseCargoError(Exception):
	"""
	Exception raised when Cargo can not be released from expected or reserved cargo lists
	"""
	pass


class CargoNotReservedError(Exception):
	"""
	Exception raised when Cargo tried to be transferred without being reserved from Storage
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

	def update(self):
		pass

	@property
	def obj_info(self) -> str:
		capacity = '; '.join([f'{k.__name__}: {v}' for k, v in self.capacity.items()])
		reserved_space = '; '.join([f'{t.__name__}: {self.get_reserved_space_by_class(t)}' for t in self.storage_types_tuple])
		filled_space = '; '.join([f'{t.__name__}: {self.get_filled_space_by_class(t)}' for t in self.storage_types_tuple])
		available_space = '; '.join([f'{t.__name__}: {self.get_available_space_by_class(t)}' for t in self.storage_types_tuple])
		items = '\n\t\t'.join([str(i) + f"({q})" for i, q in self.stored_cargo.item_dict.items()])
		return f"{super().obj_info}:\n\tC=({capacity});\n\tRS=({reserved_space});\n\tOS=({filled_space});\n\tAS=({available_space});\n\t\t{items}"

	def __str__(self):
		return f"{self.obj_info_short}"

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
	def reserved_cargo(self) -> Cargo:
		item_dict = dict()
		for c in self.reserved_cargo_list:
			for k, v in c.item_dict.items():
				item_dict[k] = item_dict.get(k) + v
		return Cargo(item_dict=item_dict)

	@property
	def expected_cargo(self) -> Cargo:
		item_dict = dict()
		for c in self.expected_cargo_list:
			for k, v in c.item_dict.items():
				item_dict[k] = item_dict.get(k) + v
		return Cargo(item_dict=item_dict)

	@property
	def available_cargo(self) -> Cargo:
		self.log.debug(f"{self.stored_cargo}, {self.reserved_cargo_list}")
		item_dict = deepcopy(self.stored_cargo.item_dict)

		for item, qty in item_dict.items():
			for reserved_cargo in self.reserved_cargo_list:
				item_dict[item] = qty - reserved_cargo.item_dict[item]

		return Cargo(item_dict=item_dict)

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
				raise NotEnoughSpaceError(
					f"Can not reserve space for cargo since there's not enough space in {cls.__name__} storage!\n"
					f"Available space: {self.get_available_space_by_class(cls)}\n"
					f"Required space: {cargo.get_total_volume_by_class(cls)}"
				)

		self.expected_cargo_list.append(cargo)
		cargo.parent_env = self

		return True

	def release_expected_cargo(self, cargo: Cargo):
		"""
		Releases (removes) expected cargo from expected_cargo_list if it was in there
		:param cargo: Cargo (an item set) to release from expected cargo list
		:return: True if successful
		"""
		res = False
		if cargo in self.expected_cargo_list:
			self.expected_cargo_list.remove(cargo)
			res = True
		else:
			raise CanNotReleaseCargoError(f"Can not release cargo from expected cargo list since it was not expected!")

		return res

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
		self.release_expected_cargo(cargo)

		# Delete cargo object
		self.delete(cargo)

		return True

	def reserve_cargo(self, cargo: Cargo) -> bool:
		"""
		Attempts to add Cargo to reserved_cargo_list for Item reservation.
		If there is not enough items available (in stored_cargo.item_dict) then method raises CanNotReserveCargoError.
		:param cargo: Cargo (an item set) to reserve from available cargo
		:return: True if successful
		"""

		res = False

		try:
			res = bool(self.available_cargo - cargo)
			self.reserved_cargo_list.append(cargo)
			cargo.parent_env = self
		except CargoSubtractionError as err:
			self.log.error(f"[{self.cls_name()}] {err}")
			raise CanNotReserveCargoError("Can not reserve cargo since there is not enough items available!")

		return res

	def release_reserve_cargo(self, cargo: Cargo):
		"""
		Releases (removes) reserved cargo from reserved_cargo_list if it was in there
		:param cargo: Cargo (an item set) to release from expected cargo list
		:return: True if successful
		"""
		res = False
		if cargo in self.reserved_cargo_list:
			self.reserved_cargo_list.remove(cargo)
			res = True
		else:
			raise CanNotReleaseCargoError(f"Can not release cargo from reserved cargo list since it was not reserved!")

		return res

	def transfer_cargo(self, cargo: Cargo):
		"""
		Attempts to transfer reserved Cargo.
		If Cargo was not reserved (not in reserved_cargo_list) then method raises CargoNotReservedError.
		:param cargo: Cargo (an item set) to store
		:return: True if successful
		"""

		# Check if cargo expected
		if cargo not in self.reserved_cargo_list:
			raise CargoNotReservedError("Can not transfer cargo since it was not reserved!")

		# Store cargo
		self.stored_cargo -= cargo

		# Free space
		self.release_reserve_cargo(cargo)

		return True
