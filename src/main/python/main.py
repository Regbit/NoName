from entity.building import Building
from entity.celestialobject import Planet
from entity.storage import *
from entity.item import *
from entity.transport import *
from tools import set_attribute_for_all_elements


def common_test_1():
	pl = Planet(name='The Planet', mass=1.0, density=1.0)
	b = Building(name='Some Building', parent_env=pl)
	print(f"{b}, {b.parent_env}, {pl.radius}")


def storage_test_1():
	st_a = Storage(capacity={Goods: 100, Ore: 0, Gas: 0})
	st_b = Storage(capacity={Goods: 50, Ore: 0, Gas: 0})
	c = Cargo(item_list=[IronBar(quantity=50001)])

	st_a.store_cargo(c)
	print(st_a)
	print(c)

	st_b.store_cargo(c)
	print(st_b)

	print(st_a.stored_cargo is st_b.stored_cargo)


def storage_test_2():
	st = Storage(capacity={Goods: 100, Ore: 0, Gas: 0})
	c_1 = Cargo(item_list=[IronBar(quantity=50000)])
	c_2 = Cargo(item_list=[IronBar(quantity=30)])

	print(st)
	st.expect_cargo(c_1)
	print(st)
	st.store_cargo(c_1)
	print(st)
	try:
		st.store_cargo(c_2)
	except CargoNotExpectedError as err:
		print(f"Error: {err}")

	print("-" * 25)
	i = 0
	for e in Entity.entity_list:
		print(f"{i}: {e}")
		i += 1

	print("-" * 25)


def rover_test_1():
	r_1 = ScavengerMKI()
	r_2 = ScavengerMKI()
	r_3 = ScavengerMKII()

	print(r_1)
	print(r_2)
	print(r_3)
	print(r_1.storage is r_2.storage)

	print(Entity.entity_list)


def tools_test_1():
	lst = [Entity(), Entity(), Entity()]
	par = Entity()
	set_attribute_for_all_elements(lst, 'parent_env', par)

	for e in lst:
		print(e)
