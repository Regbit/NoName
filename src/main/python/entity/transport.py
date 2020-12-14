from abc import ABC
from entity.entity import WorldEntity
from entity.storage import Storage
from entity.item import Goods, Ore, Gas


class Vehicle(WorldEntity, ABC):

	attributes_dict = WorldEntity.attributes_dict_copy()
	attributes_dict['storage'] = lambda x: isinstance(x, Storage), Storage()
	base_name = 'Vehicle'
	max_payload_mass = 0.0
	storage_capacity = {Goods: 0.0, Ore: 0.0, Gas: 0.0}

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			pos: Vector3,
			destination_pos: Vector3
			storage: Storage
		}
		"""
		self.storage = None
		self.max_payload_mass = None
		kwargs['storage'] = Storage(capacity=self.storage_capacity)
		kwargs['storage'].parent_env = self
		super().__init__(**kwargs)

	@property
	def total_mass(self):
		return self.mass + self.storage.total_stored_mass

	def __str__(self):
		return f"{self.obj_info}: M={self.mass}; P={self.pos};\n{self.storage}"


class Rover(Vehicle, ABC):

	base_name = 'Rover'


class ScavengerMKI(Rover):

	base_name = 'Scavenger MKI'
	mass = 2500.0
	volume = 25.0
	max_speed = 230.0
	max_payload_mass = 1500.0
	storage_capacity = {Goods: 5, Ore: 0.0, Gas: 0.0}


class ScavengerMKII(Rover):

	base_name = 'Scavenger MKII'
	mass = 2200.0
	volume = 24.0
	max_speed = 280.0
	max_payload_mass = 1750.0
	storage_capacity = {Goods: 7.5, Ore: 0.0, Gas: 0.0}
