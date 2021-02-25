from abc import ABC
from com.nng.entity.entity import Entity
from com.nng.entity.cargo import Cargo


class Request(Entity, ABC):

	base_name = 'Request'

	request_list = list()

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity
		}
		"""
		super().__init__(**kwargs)

		self.request_list.append(self)

	@property
	def requesting_entity(self):
		return self.parent_env


class CargoRequest(Request):

	attributes_dict = Request.attributes_dict_copy()
	attributes_dict['cargo'] = lambda x: isinstance(x, Cargo) and not Cargo.is_empty, Cargo

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			Request: int
		}
		"""
		self.cargo: Cargo = None
		super().__init__(**kwargs)
