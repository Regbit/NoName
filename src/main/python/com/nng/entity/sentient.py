from abc import ABC
from com.nng.entity.worldentity import WorldEntity


class Sentient(WorldEntity, ABC):
	pass


class Person(Sentient):
	pass
