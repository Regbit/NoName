from abc import ABC
from com.nng.entity.item import Goods, Ore, Gas
from com.nng.entity.massedentity import MassedEntity
from com.nng.entity.storage import Storage
from com.nng.position import Vector3


class CantSetDestinationError(Exception):
	pass


class WorldEntity(MassedEntity, ABC):
	"""
	Extension of MassedEntity class to represent entities that can be placed in the world and can move around
	"""

	attributes_dict = MassedEntity.attributes_dict_copy()
	attributes_dict['pos'] = lambda x: isinstance(x, Vector3), Vector3()
	attributes_dict['can_move'] = lambda x: isinstance(x, bool), True
	attributes_dict['path'] = lambda x: isinstance(x, list), list()
	attributes_dict['storage'] = lambda x: isinstance(x, Storage), Storage()
	base_name = 'World entity'
	mass = 0.0
	volume = 0.0
	max_speed = 0.0
	max_payload_mass = 0.0
	storage_capacity = {Goods: 0.0, Ore: 0.0, Gas: 0.0}

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			pos: Vector3,
			can_move: bool,
			path: list
		}
		"""

		self.pos: Vector3 = None
		self.can_move: bool = None
		self.path: list = None
		self.storage: Storage = None
		kwargs['storage'] = Storage(capacity=self.storage_capacity, parent_env=self)
		super().__init__(**kwargs)

	@property
	def total_mass(self):
		return self.mass + self.storage.total_stored_mass

	def __str__(self):
		return f"{self.obj_info}: M={self.mass}; P={self.pos};\n{self.storage}"

	def can_reach(self, destination):
		# TODO Placeholder. Write logic considering Vehicle type (can go to space?)
		return self.can_move

	def build_path(self, destination) -> list:
		# TODO Placeholder. Write logic that builds a path to object
		return [destination]

	def set_destination(self, destination):
		res = False

		if not isinstance(destination, (WorldEntity, Vector3)):
			raise CantSetDestinationError(
				f"Cat set destination for Entity '{self.obj_info_short}' "
				f"since destination is not WorldEntity nor Vector3!"
			)
		if not self.can_reach(destination):
			raise CantSetDestinationError(
				f"Cat set destination for Entity '{self.obj_info_short}' "
				f"since destination '{destination.obj_info_short()}' can not be reached!"
			)

		self.path = self.build_path(destination)

		res = True

		return res

	def draw(self):
		raise NotImplementedError(f'Method draw() was not implemented in class "{self.__class__.__name__}"')

	def move(self):
		raise NotImplementedError(f'Method move() was not implemented in class "{self.__class__.__name__}"')
