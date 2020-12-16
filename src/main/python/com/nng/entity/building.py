from abc import ABC
from com.nng.entity.worldentity import WorldEntity
from com.nng.entity.item import Goods, Ore, Gas


class Building(WorldEntity, ABC):

	attributes_dict = WorldEntity.attributes_dict_copy()
	attributes_dict.pop('can_move')
	base_name = 'Building'
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
			path: list
		}
		"""
		kwargs['can_move'] = False
		super().__init__(**kwargs)


class Warehouse(Building, ABC):

	base_name = 'Warehouse'
	storage_capacity = {Goods: 1000.0, Ore: 10000.0, Gas: 0.0}


class Miner(Building, ABC):

	base_name = 'Miner'
	storage_capacity = {Goods: 100.0, Ore: 1000.0, Gas: 0.0}
