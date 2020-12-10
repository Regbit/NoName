from abc import ABC
from src.entity.entity import WorldEntity
from math import pi


class CelestialObject(WorldEntity, ABC):

	attributes_dict = WorldEntity.attributes_dict
	attributes_dict['density'] = lambda x: isinstance(x, (float, int)) and x > 0, 0.0

	e_mass_kg = 5.97 * (10 ** 24)
	e_density_kg_per_sm3 = 5.51 / 1000

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
			max_speed: float,
			density: float
		}
		"""
		# TODO Keep only one: Density or Volume
		self.density = None
		super().__init__(**kwargs)
		self.radius = self.calc_radius(self.mass, self.density)

	@classmethod
	def calc_radius(cls, mass, density):
		"""
		Return radius in kilometers
		:param mass: relative to Earth's mass
		:param density: relative to Earth's density
		:return: radius - sphere's radius in kilometers
		"""
		# V = 4/3 * pi * r**3
		# r ** 3 = V / (4/3 * pi)
		# r = (V / (4/3 * pi)) ** (1/3)
		# V = mass / density
		# r = (mass / density / (4/3 * pi)) ** (1/3)
		return round(
			((mass * cls.e_mass_kg) / (density * cls.e_density_kg_per_sm3) / (4/3 * pi)) ** (1/3) / 100000,
			4
		)


class Star(CelestialObject):
	pass


class Planet(CelestialObject):
	pass
