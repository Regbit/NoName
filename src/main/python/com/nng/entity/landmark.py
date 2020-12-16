from abc import ABC
from com.nng.entity.worldentity import WorldEntity


class Landmark(WorldEntity, ABC):

	base_name = 'Landmark'

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			pos: Vector3
		}
		"""

		kwargs['can_move'] = False
		kwargs['destination_pos'] = None
		super().__init__(**kwargs)


class ResourceNode(Landmark):

	base_name = 'Resource node'
