from abc import ABC
from entity.worldentity import WorldEntity
from entity.item import Goods, Ore, Gas


class Vehicle(WorldEntity, ABC):

	base_name = 'Vehicle'


class Rover(Vehicle, ABC):

	base_name = 'Rover'


class ScavengerMKI(Rover):

	base_name = 'Scavenger MKI'
	mass = 2500.0
	volume = 25.0
	max_speed = 230.0
	max_payload_mass = 1500.0
	storage_capacity = {Goods: 5, Ore: 0.0, Gas: 0.0}


class ScavengerMKII(Rover):

	base_name = 'Scavenger MKII'
	mass = 2200.0
	volume = 24.0
	max_speed = 280.0
	max_payload_mass = 1750.0
	storage_capacity = {Goods: 7.5, Ore: 0.0, Gas: 0.0}
