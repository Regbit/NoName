from abc import ABC
from position import Vector3
from copy import deepcopy


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

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity
		}
		"""

		try:
			self.name: str = None
			self.parent_env: Entity = None

			kwargs.update(self.class_desc())

			for name, meta in self.attributes_dict.items():
				if kwargs.get(name) and meta[0](kwargs.get(name)):
					self.__setattr__(name, kwargs.get(name))
				elif kwargs.get(name) and not meta[0](kwargs.get(name)):
					raise AttributeTypeError(f'Attribute {name} was not set! Input value: {kwargs.get(name)}')
				else:
					self.__setattr__(name, deepcopy(meta[1]))
		except AttributeTypeError as err:
			# TODO Figure out what tot do here. Maybe use Logger.
			# print(err)
			pass

		self.entity_list.append(self)

	@property
	def obj_info_short(self):
		return f"{type(self).__name__} #..{str(self.__hash__())[-5:]}"

	@property
	def obj_info(self):
		return self.obj_info_short + (f" ({self.parent_env.obj_info_short})" if self.parent_env else '')

	def __str__(self):
		return f'{self.obj_info}: N="{self.name}"'

	@classmethod
	def attributes_dict_copy(cls):
		return deepcopy(cls.attributes_dict)

	@classmethod
	def make(cls, **kwargs):
		"""
		Safe initialization of an object. New object added to Entity.entity_list.
		:param kwargs: see __init__ description
		:return:
		"""
		try:
			new = cls(**kwargs)
			cls.entity_list.append(new)
			return new
		except AttributeTypeError as err:
			# TODO Figure out what tot do here. Maybe use Logger.
			# print(err)
			pass

	@classmethod
	def delete(cls, *args):
		"""
		Delete reference to all input Entity objects.
		:param args: Entity array
		:return:
		"""
		for e in args:
			if isinstance(e, Entity):
				e.entity_list.remove(e)
				del e

	@classmethod
	def class_desc(cls):
		return {}

	def update(self):
		raise NotImplementedError(f'Method update() was not implemented in class "{self.__class__.__name__}"')


class MassedEntity(Entity, ABC):
	"""
	Extension of Entity class to represent physically affective entities
	"""

	attributes_dict = Entity.attributes_dict_copy()
	attributes_dict['mass'] = lambda x: isinstance(x, (float, int)) and x > 0, 0.0
	attributes_dict['volume'] = lambda x: isinstance(x, (float, int)) and x > 0, 0.0

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			mass: float,
			volume: float
		}
		"""
		self.mass: float = None
		self.volume: float = None
		super().__init__(**kwargs)

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

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			mass: float,
			volume: float,
			pos: Vector3,
			can_move: bool,
			destination_pos: Vector3,
			max_speed: float
		}
		"""

		self.pos: Vector3 = None
		self.can_move: bool = None
		self.destination_pos: Vector3 = None
		self.max_speed: float = None
		super().__init__(**kwargs)

	def set_destination(self, destination):
		if isinstance(destination, Entity):
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
