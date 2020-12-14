from abc import ABC
from position import Vector3
from copy import deepcopy
import logging


class AttributeTypeError(Exception):
	pass


class Entity(ABC):
	"""
	Base abstract class for game entities
	"""

	entity_list = list()
	attributes_dict = dict()
	attributes_dict['name'] = lambda x: isinstance(x, str), None
	attributes_dict['parent_env'] = lambda x: issubclass(type(x), Entity), None
	base_name = 'Entity'
	log = logging.getLogger(__name__)

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity
		}
		"""

		self.log.info(f"[{self.cls_name()}] Initializing...")
		self.log.debug(f"[{self.cls_name()}] kwargs = {kwargs}")

		try:
			self.name: str = None
			self.parent_env: Entity = None

			for name, meta in self.attributes_dict.items():
				if kwargs.get(name) and meta[0](kwargs.get(name)):
					self.__setattr__(name, kwargs.get(name))
				elif kwargs.get(name) and not meta[0](kwargs.get(name)):
					raise AttributeTypeError(f'Attribute "{name}" was not set! Input value: {kwargs.get(name)}')
				else:
					attr_copy = deepcopy(meta[1])
					if issubclass(type(attr_copy), Entity) and attr_copy not in self.entity_list:
						self.entity_list.append(attr_copy)
					self.log.debug(f'[{self.cls_name()}] Attribute "{name}" was not input. Setting default value: {attr_copy}')
					self.__setattr__(name, attr_copy)

			self.entity_list.append(self)
			self.log.debug(f"[{self.cls_name()}] entity_list = {self.entity_list}")
			self.log.info(f"[{self.cls_name()}] Success!")
		except AttributeTypeError as err:
			self.log.warning(f"[{self.cls_name()}] Could not make instance! Error message: {err}")

	@classmethod
	def cls_name(cls):
		return cls.__name__

	@property
	def obj_info_short(self):
		return f"{self.base_name} #..{str(self.__hash__())[-5:]}"

	@property
	def obj_info(self):
		return self.obj_info_short + (f" ({self.parent_env.obj_info_short})" if self.parent_env else '')

	def __str__(self):
		return f'{self.obj_info}: N="{self.name}"'

	@classmethod
	def attributes_dict_copy(cls):
		return deepcopy(cls.attributes_dict)

	@classmethod
	def delete(cls, *args):
		"""
		Delete reference to all input Entity objects.
		:param args: Entity array
		:return:
		"""
		cls.log.info(f"[{cls.cls_name()}] Deleting objects: {args}")
		for e in args:
			if isinstance(e, Entity):
				e.entity_list.remove(e)
				del e
				cls.log.info(f"[{cls.cls_name()}] Success!")
			else:
				cls.log.warning(f"[{cls.cls_name()}] Object {e} is not Entity subclass!")

	def update(self):
		raise NotImplementedError(f'Method update() was not implemented in class "{self.__class__.__name__}"')


class MassedEntity(Entity, ABC):
	"""
	Extension of Entity class to represent entities affected by physics
	"""

	attributes_dict = Entity.attributes_dict_copy()
	base_name = 'Massed Entity'
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


class WorldEntity(MassedEntity, ABC):
	"""
	Extension of MassedEntity class to represent entities that can be placed in the world and can move around
	"""

	attributes_dict = MassedEntity.attributes_dict_copy()
	attributes_dict['pos'] = lambda x: isinstance(x, Vector3), Vector3()
	attributes_dict['can_move'] = lambda x: isinstance(x, bool), True
	attributes_dict['destination_pos'] = lambda x: isinstance(x, Vector3), Vector3()
	attributes_dict['max_speed'] = lambda x: isinstance(x, (float, int)) and x > 0, 0.0
	base_name = 'World Entity'
	mass = 0.0
	volume = 0.0
	max_speed = 0.0

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			pos: Vector3,
			can_move: bool,
			destination_pos: Vector3
		}
		"""

		self.pos: Vector3 = None
		self.can_move: bool = None
		self.destination_pos: Vector3 = None
		super().__init__(**kwargs)

	def set_destination(self, destination):
		if isinstance(destination, WorldEntity):
			self.destination_pos = destination.pos
		elif isinstance(destination, Vector3):
			self.destination_pos = destination
		else:
			return False
		return True

	def draw(self):
		raise NotImplementedError(f'Method draw() was not implemented in class "{self.__class__.__name__}"')

	def move(self):
		raise NotImplementedError(f'Method move() was not implemented in class "{self.__class__.__name__}"')


class ResourceNode(WorldEntity):
	pass
