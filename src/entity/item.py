from abc import ABC
from src.entity.entity import MassedEntity


class Item(MassedEntity, ABC):

	attributes_dict = MassedEntity.attributes_dict
	attributes_dict['quantity'] = lambda x: isinstance(x, int) and x > 0, 0

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			mass: float,
			volume: float,
			quantity: int
		}
		"""
		self.quantity = None
		super().__init__(**kwargs)

	def __str__(self):
		return f"{self.obj_info}: M={self.mass}; V={self.volume}; Q={self.quantity}"

	def update(self):
		pass

	@property
	def total_volume(self):
		return self.volume * self.quantity

	@property
	def total_mass(self):
		return self.mass * self.quantity


class Goods(Item, ABC):
	pass


class IronBar(Goods):

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			parent_env: Entity,
			quantity: int
		}
		"""
		kwargs['name'] = 'Iron bar'
		kwargs['mass'] = 1
		kwargs['volume'] = 0.001
		super().__init__(**kwargs)


class Ore(Item, ABC):
	pass


class IronOre(Ore):

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			parent_env: Entity,
			quantity: int
		}
		"""
		kwargs['name'] = 'Iron ore'
		kwargs['mass'] = 1000
		kwargs['volume'] = 0.1
		super().__init__(**kwargs)


class Gas(Item, ABC):
	pass
