from abc import ABC
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
		Initialization of an object. New object is added to Entity.entity_list.
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
					raise AttributeTypeError(f'Attribute "{name}" was not set! Input value: {kwargs.get(name)}. Expected: {meta[1]}')
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
	def hash(self):
		return f"#..{str(self.__hash__())[-5:]}"

	@property
	def obj_info_short(self):
		return f"{self.base_name} {self.hash}" + (f" ({self.parent_env.obj_info_short})" if self.parent_env else '')

	@property
	def obj_info(self):
		# TODO Remove redundant methods
		return self.obj_info_short

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
		cls.log.info(f"[{cls.cls_name()}] Deleting {len(args)} object{'s' if len(args) > 1 else ''}...")
		for e in args:
			cls.log.info(f"[{cls.cls_name()}] Attempting to delete '{e.obj_info_short}'...")
			if isinstance(e, Entity):
				e.entity_list.remove(e)
				del e
				cls.log.info(f"[{cls.cls_name()}] Success!")
			else:
				cls.log.warning(f"[{cls.cls_name()}] Object {e} is not Entity subclass!")

	@classmethod
	def update_all(cls):
		for e in cls.entity_list:
			e.update()

	@classmethod
	def print_all(cls):
		for i, e in zip(range(len(cls.entity_list)), cls.entity_list):
			print(f"{i}: {e}")

	def update(self):
		raise NotImplementedError(f'Method update() was not implemented in class "{self.__class__.__name__}"')
