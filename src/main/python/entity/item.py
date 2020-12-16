from abc import ABC
from entity.massedentity import MassedEntity


class Item(MassedEntity, ABC):

	base_name = 'Item'


class Goods(Item, ABC):

	base_name = 'Goods'


class IronBar(Goods, ABC):

	base_name = 'Iron bar'
	mass = 1
	volume = 0.001


class Ore(Item, ABC):

	base_name = 'Ore'


class IronOre(Ore, ABC):

	base_name = 'Iron ore'
	mass = 1000
	volume = 0.1


class Gas(Item, ABC):

	base_name = 'Gas'
