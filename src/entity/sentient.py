from abc import ABC
from src.entity.entity import WorldEntity


class Sentient(WorldEntity, ABC):
	pass


class Person(Sentient):
	pass
