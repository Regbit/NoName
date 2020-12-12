from abc import ABC
from entity.entity import WorldEntity
from entity.storage import Storage
from entity.item import Goods, Ore, Gas


class Vehicle(WorldEntity, ABC):

	attributes_dict = WorldEntity.attributes_dict_copy()
	attributes_dict['storage'] = lambda x: isinstance(x, Storage), Storage()
	attributes_dict['max_payload_mass'] = lambda x: isinstance(x, (float, int)) and x > 0, 0.0

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			mass: float,
			volume: float,
			pos: Vector3,
			destination_pos: Vector3,
			max_speed: float,
			storage: Storage,
			max_payload_mass: float
		}
		"""
		self.storage = None
		self.max_payload_mass = None
		super().__init__(**kwargs)
		self.storage.parent_env = self

	@property
	def total_mass(self):
		return self.mass + self.storage.total_mass

	def __str__(self):
		return f"{self.obj_info}: M={self.mass}; P={self.pos};\n{self.storage}"


class Rover(Vehicle, ABC):

	@classmethod
	def class_desc(cls):
		if cls is ScavengerMKI:
			return {
				'name': 'Scavenger MKI',
				'mass': 2500,
				'volume': 25,
				'max_speed': 230,
				'storage': Storage.make(capacity={Goods: 5, Ore: 0.0, Gas: 0.0}),
				'max_payload_mass': 1500
			}
		elif cls is ScavengerMKII:
			return {
				'name': 'Scavenger MKII',
				'mass': 2200,
				'volume': 24,
				'max_speed': 280,
				'storage': Storage.make(capacity={Goods: 7.5, Ore: 0.0, Gas: 0.0}),
				'max_payload_mass': 1750
			}
		else:
			return dict()


class ScavengerMKI(Rover):
	pass


class ScavengerMKII(Rover):
	pass
