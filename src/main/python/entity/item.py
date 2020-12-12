from abc import ABC
from src.main.python.entity.entity import MassedEntity


class Item(MassedEntity, ABC):

	def update(self):
		pass


class Goods(Item, ABC):

	@classmethod
	def class_desc(cls):
		if cls is IronBar:
			return {
				'name': 'Iron bar',
				'mass': 1,
				'volume': 0.001
			}
		else:
			return {}


class IronBar(Goods):
	pass


class Ore(Item, ABC):

	@classmethod
	def class_desc(cls):
		if cls is IronOre:
			return {
				'name': 'Iron ore',
				'mass': 1000,
				'volume': 0.1
			}
		else:
			return {}


class IronOre(Ore):
	pass


class Gas(Item, ABC):
	pass
