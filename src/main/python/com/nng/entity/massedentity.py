from abc import ABC
from com.nng.entity.entity import Entity


class MassedEntity(Entity, ABC):
	"""
	Extension of Entity class to represent entities affected by physics
	"""

	attributes_dict = Entity.attributes_dict_copy()
	base_name = 'Massed entity'
	mass = 0.0
	volume = 0.0

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity
		}
		"""
		super().__init__(**kwargs)

	@classmethod
	def cls_name(cls):
		return f"{cls.__name__}: M={cls.mass}; V={cls.volume}"

	def __str__(self):
		return f"{self.obj_info}: M={self.mass}; V={self.volume}"
