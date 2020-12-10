from src.entity.entity import Building
from src.entity.celestialobject import Planet
from src.entity.storage import *
from src.entity.item import *
from src.entity.transport import *
from src.tools import set_attribute_for_all_elements


def common_test_1():
	pl = Planet.make(name='The Planet', mass=1.0, density=1.0)
	b = Building.make(name='Some Building', parent_env=pl)
	print(f"{b}, {b.parent_env}, {pl.radius}")


def storage_test_1():
	st_a = Storage(capacity={Goods: 100, Ore: 0, Gas: 0})
	st_b = Storage(capacity={Goods: 50, Ore: 0, Gas: 0})
	c = Cargo(item_list=[IronBar(quantity=50001)])

	st_a.store(c)
	print(st_a)
	print(c)

	st_b.store(c)
	print(st_b)

	print(st_a.stored_items_list is st_b.stored_items_list)


def storage_test_2():
	st = Storage.make(capacity={Goods: 100, Ore: 0, Gas: 0})
	c_1 = Cargo.make(item_list=[IronBar.make(quantity=50000)])
	c_2 = Cargo.make(item_list=[IronBar.make(quantity=30)])

	print(st)
	st.expect_cargo(c_1)
	print(st)
	st.store(c_1)
	print(st)
	try:
		st.store(c_2)
	except CargoNotExpectedError as err:
		print(f"Error: {err}")

	print("-" * 25)
	i = 0
	for e in Entity.entity_list:
		print(f"{i}: {e}")
		i += 1

	print("-" * 25)


def rover_test_1():
	r = Rover.make(**RoverClass.ScavengerMKI)

	print(r)


def tools_test_1():
	lst = [Entity.make(), Entity.make(), Entity.make()]
	par = Entity.make()
	set_attribute_for_all_elements(lst, 'parent_env', par)

	for e in lst:
		print(e)


print(type(lambda x: isinstance(x, str)).__name__)
