from abc import ABC
from com.nng.entity.worldentity import WorldEntity
from com.nng.tools import calc_radius


class CelestialObject(WorldEntity, ABC):

	base_name = 'Celestial object'
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
			destination_pos: Vector3,
			max_speed: float
		}
		"""

		super().__init__(**kwargs)
		self.radius = calc_radius(self.mass, self.volume)


class Star(CelestialObject, ABC):

	base_name = 'Star'
	mass = 0.0
	volume = 0.0
	max_speed = 0.0


class Planet(CelestialObject, ABC):

	base_name = 'Planet'
	mass = 0.0
	volume = 0.0
	max_speed = 0.0
