from abc import ABC
from src.entity.entity import WorldEntity
from src.entity.storage import Storage
from src.entity.item import Goods, Ore, Gas


class Vehicle(WorldEntity, ABC):

	attributes_dict = WorldEntity.attributes_dict
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

	def __str__(self):
		return f"{self.obj_info}: M={self.mass}; P={self.pos};\n{self.storage}"


class Rover(Vehicle, ABC):
	pass


class RoverClass(ABC):

	ScavengerMKI = {
		'name': 'Scavenger MKI',
		'mass': 2500,
		'volume': 25,
		'max_speed': 230,
		'storage': Storage.make(capacity={Goods: 5, Ore: 0.0, Gas: 0.0}),
		'max_payload_mass': 1500

	}


class ScavengerMKI(Rover):

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			parent_env: Entity,
			pos: Vector3,
			destination_pos: Vector3
		}
		"""

		kwargs['name'] = 'Scavenger MKI'
		kwargs['mass'] = 2500
		kwargs['volume'] = 25
		kwargs['max_speed'] = 230
		kwargs['storage'] = Storage.make(parent_env=self, capacity={Goods: 5, Ore: 0.0, Gas: 0.0})
		kwargs['max_payload_mass'] = 1500
		super().__init__(**kwargs)


class ScavengerMKII(Rover):

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			parent_env: Entity,
			pos: Vector3,
			destination_pos: Vector3
		}
		"""

		kwargs['name'] = 'Scavenger MKII'
		kwargs['mass'] = 2200
		kwargs['volume'] = 24
		kwargs['max_speed'] = 280
		kwargs['storage'] = Storage.make(parent_env=self, capacity={Goods: 7.5, Ore: 0.0, Gas: 0.0})
		kwargs['max_payload_mass'] = 1750
		super().__init__(**kwargs)
