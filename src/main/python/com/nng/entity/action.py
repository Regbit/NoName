from abc import ABC
from com.nng.entity.entity import Entity
from com.nng.entity.cargo import Cargo
from com.nng.entity.storage import NotEnoughSpaceError, CanNotReleaseCargoError, CanNotReserveCargoError
from com.nng.entity.worldentity import WorldEntity, CantSetDestinationError
from com.nng.position import Vector3


class Action(Entity, ABC):

	QUEUED = 0
	SUCCESS = 1
	IN_PROGRESS = 2
	FAILURE = 3
	REVERSED = 4

	attributes_dict = Entity.attributes_dict_copy()
	attributes_dict['status'] = lambda x: isinstance(x, int) and Action.QUEUED <= x <= Action.REVERSED, QUEUED
	attributes_dict['is_continuous'] = lambda x: isinstance(x, bool), False

	base_name = 'Action'

	task_list = list()

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			status: int,
			is_continuous: bool
		}
		"""
		self.status: int = None
		self.is_continuous: bool = None
		super().__init__(**kwargs)

	def perform(self):
		raise NotImplementedError(f'Method perform() was not implemented in class "{self.__class__.__name__}"')

	def revert(self):
		raise NotImplementedError(f'Method revert() was not implemented in class "{self.__class__.__name__}"')


class CheckIfCanReachAction(Action):

	attributes_dict = Action.attributes_dict_copy()
	attributes_dict.pop('status')
	attributes_dict.pop('is_continuous')
	attributes_dict['entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['destination'] = lambda x: isinstance(x, (WorldEntity, Vector3)), None

	base_name = 'Check if can reach action'

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			entity: WorldEntity,
			destination: WorldEntity or Vector3
		}
		"""
		self.entity: WorldEntity = None
		self.destination = None
		super().__init__(**kwargs)

	def perform(self):
		if self.entity.can_reach(self.destination):
			self.status = Action.SUCCESS
		else:
			self.status = Action.FAILURE

	def revert(self):
		pass


class SetDestinationAction(Action):

	attributes_dict = Action.attributes_dict_copy()
	attributes_dict.pop('status')
	attributes_dict.pop('is_continuous')
	attributes_dict['entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['destination'] = lambda x: isinstance(x, (WorldEntity, Vector3)), None

	base_name = 'Set destination action'

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			entity: WorldEntity,
			destination: WorldEntity or Vector3
		}
		"""
		self.entity: WorldEntity = None
		self.destination = None
		super().__init__(**kwargs)

	def perform(self):
		try:
			self.entity.set_destination(self.destination)
			self.status = Action.SUCCESS
		except CantSetDestinationError as e:
			# TODO raise some error?
			self.status = Action.FAILURE

	def revert(self):
		self.entity.path = list()
		self.status = Action.REVERSED


class ExpectCargoAction(Action):

	attributes_dict = Action.attributes_dict_copy()
	attributes_dict.pop('status')
	attributes_dict.pop('is_continuous')
	attributes_dict['entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['cargo'] = lambda x: isinstance(x, Cargo), None

	base_name = 'Expect cargo action'

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			entity: WorldEntity,
			cargo: cargo
		}
		"""
		self.entity: WorldEntity = None
		self.cargo: Cargo = None
		super().__init__(**kwargs)

	def perform(self):
		try:
			self.entity.storage.expect_cargo(self.cargo)
			self.status = Action.SUCCESS
		except NotEnoughSpaceError as e:
			# TODO raise some error?
			self.status = Action.FAILURE

	def revert(self):
		try:
			self.entity.storage.release_expected_cargo(self.cargo)
		except CanNotReleaseCargoError as e:
			# TODO raise some error?
			pass
		self.status = Action.REVERSED


class ReserveCargoAction(Action):

	attributes_dict = Action.attributes_dict_copy()
	attributes_dict.pop('status')
	attributes_dict.pop('is_continuous')
	attributes_dict['entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['cargo'] = lambda x: isinstance(x, Cargo), None

	base_name = 'Reserve cargo action'

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			entity: WorldEntity,
			cargo: cargo
		}
		"""
		self.entity: WorldEntity = None
		self.cargo: Cargo = None
		super().__init__(**kwargs)

	def perform(self):
		try:
			self.entity.storage.reserve_cargo(self.cargo)
			self.status = Action.SUCCESS
		except CanNotReserveCargoError as e:
			# TODO raise some error?
			self.status = Action.FAILURE

	def revert(self):
		try:
			self.entity.storage.release_reserve_cargo(self.cargo)
		except CanNotReleaseCargoError as e:
			# TODO raise some error?
			pass
		self.status = Action.REVERSED


class MoveAction(Action):

	attributes_dict = Action.attributes_dict_copy()
	attributes_dict.pop('status')
	attributes_dict.pop('is_continuous')
	attributes_dict['entity'] = lambda x: isinstance(x, WorldEntity), None

	base_name = 'Move action'

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			entity: WorldEntity
		}
		"""
		self.entity: WorldEntity = None
		kwargs['is_continuous'] = True
		super().__init__(**kwargs)

	def perform(self):
		try:
			self.entity.move()
			if len(self.entity.path):
				self.status = Action.IN_PROGRESS
			else:
				self.status = Action.SUCCESS
		except Exception as e:
			# TODO raise some error?
			self.status = Action.FAILURE

	def revert(self):
		# TODO How to revert move?
		pass


class TransferCargoAction(Action):

	attributes_dict = Action.attributes_dict_copy()
	attributes_dict.pop('status')
	attributes_dict.pop('is_continuous')
	attributes_dict['from_entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['to_entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['cargo'] = lambda x: isinstance(x, Cargo), None

	base_name = 'Transfer cargo action'

	def __init__(self, **kwargs):
		"""
		Initialization of an object. New object is added to Entity.entity_list.
		:param kwargs: {
			name: str,
			parent_env: Entity,
			from_entity: WorldEntity
			to_entity: WorldEntity
			cargo: Cargo
		}
		"""
		self.from_entity: WorldEntity = None
		self.to_entity: WorldEntity = None
		self.cargo: Cargo = None
		super().__init__(**kwargs)

	def perform(self):
		try:
			self.from_entity.storage.transfer_cargo(self.cargo)
			self.to_entity.storage.store_cargo(self.cargo)
			self.status = Action.SUCCESS
		except Exception as e:
			# TODO raise some error?
			self.status = Action.FAILURE

	def revert(self):
		# TODO Can you reverse this?
		pass