from com.nng.entity.action import *
from com.nng.entity.entity import Entity
from com.nng.entity.worldentity import WorldEntity
from com.nng.entity.cargo import Cargo


class TaskPlanningError(Exception):
	pass


class TaskHardCheckError(Exception):
	pass


class TaskSoftCheckError(Exception):
	pass


class TaskExecutionError(Exception):
	pass


class Task(Entity, ABC):

	# Priority
	CRITICAL = 0
	HIGH = 1
	MEDIUM = 2
	LOW = 3

	# Task status
	INITIALIZED = 0
	EXECUTION = 1
	SUCCESS = 2
	FAILURE = 3

	# Action type
	ACTION_HARD_CHECK = 1
	ACTION_SOFT_CHECK = 2
	ACTION_EXECUTION = 3

	attributes_dict = Entity.attributes_dict_copy()
	attributes_dict['action_list'] = lambda x: isinstance(x, list), list()
	attributes_dict['priority'] = lambda x: isinstance(x, int) and Task.CRITICAL <= x <= Task.LOW, MEDIUM
	base_name = 'Task'

	task_list = list()

	def __init__(self, **kwargs):
		self.action_list: list = None
		self.priority: int = None
		self.current_action_id = 0
		self.status = None
		super().__init__(**kwargs)

		self.task_list.append(self)

	@classmethod
	def delete(cls, *args):
		super().delete(*args)
		for t in args:
			if isinstance(t, Task):
				cls.task_list.remove(t)

	def execute(self):
		raise NotImplementedError(f'Method execute() was not implemented in class "{self.__class__.__name__}"')


class TransportTask(Task):

	attributes_dict = Task.attributes_dict_copy()
	attributes_dict['transport_entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['cargo'] = lambda x: isinstance(x, Cargo), None
	attributes_dict['from_entity'] = lambda x: isinstance(x, WorldEntity), None
	attributes_dict['to_entity'] = lambda x: isinstance(x, WorldEntity), None
	base_name = 'Transport task'

	def __init__(self, **kwargs):

		self.transport_entity: WorldEntity = None
		self.cargo: Cargo = None
		self.from_entity: WorldEntity = None
		self.to_entity: WorldEntity = None

		super().__init__(**kwargs)

		# --HARD CHECK: cancel Task if any condition is False--
		# can expect 'cargo' in 'to_entity'
		# can reserve 'cargo' in 'from_entity'
		# --SOFT CHECK: switch executor if any condition is False--
		# 'transport_entity' can reach 'from_entity'
		# 'transport_entity' can reach 'to_entity'
		# can expect 'cargo' in 'transport_entity'
		# --PLAN--
		# 'transport_entity' move to 'from_entity'
		# 'transport_entity' picks up 'cargo' from 'from_entity'
		# 'transport_entity' move to 'to_entity'
		# 'transport_entity' store 'cargo' to 'to_entity'

		try:
			# HARD CHECK
			self.action_list.append((
				ExpectCargoAction(entity=self.to_entity, cargo=self.cargo),
				Task.ACTION_HARD_CHECK
			))
			self.action_list.append((
				ReserveCargoAction(entity=self.from_entity, cargo=self.cargo),
				Task.ACTION_HARD_CHECK
			))
			# SOFT CHECK
			self.action_list.append((
				CheckIfCanReachAction(entity=self.transport_entity, destination=self.from_entity),
				Task.ACTION_SOFT_CHECK
			))
			self.action_list.append((
				CheckIfCanReachAction(entity=self.transport_entity, destination=self.to_entity),
				Task.ACTION_SOFT_CHECK
			))
			self.action_list.append((
				ExpectCargoAction(entity=self.transport_entity, cargo=self.cargo),
				Task.ACTION_SOFT_CHECK
			))
			# EXECUTION
			self.action_list.append((
				SetDestinationAction(entity=self.transport_entity, destination=self.from_entity),
				Task.ACTION_EXECUTION
			))
			self.action_list.append((
				MoveAction(entity=self.transport_entity),
				Task.ACTION_EXECUTION
			))
			self.action_list.append((
				TransferCargoAction(from_entity=self.from_entity, to_entity=self.transport_entity, cargo=self.cargo),
				Task.ACTION_EXECUTION
			))
			self.action_list.append((
				SetDestinationAction(entity=self.transport_entity, destination=self.to_entity),
				Task.ACTION_EXECUTION
			))
			self.action_list.append((
				MoveAction(entity=self.transport_entity),
				Task.ACTION_EXECUTION
			))
			self.action_list.append((
				TransferCargoAction(from_entity=self.transport_entity, to_entity=self.to_entity, cargo=self.cargo),
				Task.ACTION_EXECUTION
			))

			self.status = Task.INITIALIZED
		except Exception as e:
			raise TaskPlanningError(f"Task planning error ({type(e)}): {e}")

	def execute(self):
		if self.status in (Task.INITIALIZED, Task.EXECUTION):
			self.status = Task.EXECUTION
			action = self.action_list[self.current_action_id]

			try:
				action[0].perform()
				
				if action[0].status == Action.SUCCESS:
					self.current_action_id += 1

					if self.current_action_id >= len(self.action_list):
						self.status = Task.SUCCESS

			except Exception as e:
				self.status = Task.FAILURE
				if action[1] == Task.ACTION_HARD_CHECK:
					raise TaskHardCheckError(f"Task hard check error (Error={type(e)}; Action={action[0].obj_info_short}): {e}")
				elif action[1] == Task.ACTION_SOFT_CHECK:
					raise TaskSoftCheckError(f"Task soft check error (Error={type(e)}; Action={action[0].obj_info_short}): {e}")
				elif action[1] == Task.ACTION_EXECUTION:
					raise TaskExecutionError(f"Task execution error (Error={type(e)}; Action={action[0].obj_info_short}): {e}")


class MiningTask(Task):
	pass
