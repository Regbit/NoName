from abc import ABC
from entity.worldentity import WorldEntity


class Sentient(WorldEntity, ABC):
	pass


class Person(Sentient):
	pass
