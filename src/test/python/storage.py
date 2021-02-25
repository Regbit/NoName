from unittest import main
from src.test.python.nonametest import NoNameTestCase
from com.nng.entity.item import *
from com.nng.entity.storage import *
import logging


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s')


class CargoTest(NoNameTestCase):

	def test_cargo_class_init(self):
		cls = Cargo

		self.assertIsNotNone(cls)

		self.assertIsNotNone(cls.attributes_dict)
		self.assertIsInstance(cls.attributes_dict, dict)
		self.assertGreater(len(cls.attributes_dict), 0)

		self.assertEqual(set(cls.attributes_dict.keys()), {'name', 'parent_env', 'item_dict'})
		self.assertIsNotNone(cls.attributes_dict['name'])
		self.assertIsNotNone(cls.attributes_dict['parent_env'])
		self.assertIsNotNone(cls.attributes_dict['item_dict'])

		for k, v in cls.attributes_dict.items():
			self.assertIsInstance(v, tuple)
			self.assertEqual(len(v), 2)
			self.assertIsInstance(v[0], type(lambda x: x))

		self.assertEqual(cls.base_name, 'Cargo')

	def test_cargo_init_empty(self):
		cls = Cargo
		c = cls()
		self.assertIsNotNone(c)

		self.assertIsNone(c.name)
		self.assertIsNone(c.parent_env)

		self.assertIsNotNone(c.item_dict)
		self.assertIsInstance(c.item_dict, dict)
		self.assertTrue(c.is_empty)
		self.assertEqual(len(cls.entity_list), 1)
		self.assertIs(cls.entity_list[0], c)

	def test_cargo_init_with_attributes(self):
		cls = Cargo
		name = 'Cargo'
		parent_env = Entity()
		item_dict = dict()
		c = cls(name=name, parent_env=parent_env, item_dict=item_dict)

		self.assertIsNotNone(c)
		self.assertEqual(c.name, name)
		self.assertEqual(c.parent_env, parent_env)
		self.assertEqual(c.item_dict, item_dict)

		self.assertEqual(len(cls.entity_list), 2)
		self.assertIs(cls.entity_list[0], parent_env)
		self.assertIs(cls.entity_list[1], c)

	def test_cargo_init_with_items(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)
		self.assertFalse(c.is_empty)
		self.assertEqual(c.item_dict, item_dict)
		self.assertTrue(i_1 in c.item_dict)
		self.assertTrue(i_2 in c.item_dict)

		self.assertEqual(c.mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty)
		self.assertEqual(c.volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty)

		self.assertEqual(len(Entity.entity_list), 1)

	def test_cargo_add(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		item_dict[i_1] = i_1_qty

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_2] = i_2_qty

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		c_3 = c_1 + c_2

		self.assertIsNotNone(c_3)
		self.assertFalse(c_3.is_empty)
		self.assertIsNot(c_3.item_dict, c_1.item_dict)
		self.assertIsNot(c_3.item_dict, c_2.item_dict)
		self.assertTrue(i_1 in c_3.item_dict)
		self.assertTrue(i_1 not in c_2.item_dict)
		self.assertTrue(i_2 in c_3.item_dict)
		self.assertTrue(i_2 not in c_1.item_dict)

		self.assertEqual(c_3.mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty)
		self.assertEqual(c_3.mass, c_1.mass + c_2.mass)
		self.assertEqual(c_3.volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty)
		self.assertEqual(c_3.volume, c_1.volume + c_2.volume)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_cargo_iadd(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		item_dict[i_1] = i_1_qty

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_2] = i_2_qty

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		c_1 += c_2

		self.assertIsNotNone(c_1)
		self.assertFalse(c_1.is_empty)
		self.assertIsNot(c_1.item_dict, c_2.item_dict)
		self.assertTrue(i_1 in c_1.item_dict)
		self.assertTrue(i_1 not in c_2.item_dict)
		self.assertTrue(i_2 in c_1.item_dict)

		self.assertEqual(c_1.mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty)
		self.assertEqual(c_1.volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_cargo_sub_success(self):
		cls = Cargo
		item_dict = dict()

		i = IronBar
		i_qty_1 = 2

		item_dict[i] = i_qty_1

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_qty_2 = 1

		item_dict[i] = i_qty_2

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		c_3 = c_1 - c_2

		self.assertIsNotNone(c_3)
		self.assertFalse(c_3.is_empty)
		self.assertIsNot(c_3.item_dict, c_1.item_dict)
		self.assertIsNot(c_3.item_dict, c_2.item_dict)
		self.assertTrue(i in c_3.item_dict)

		self.assertEqual(c_3.mass, i.mass * i_qty_1 - i.mass * i_qty_2)
		self.assertEqual(c_3.mass, c_1.mass - c_2.mass)
		self.assertEqual(c_3.volume, i.volume * i_qty_1 - i.volume * i_qty_2)
		self.assertEqual(c_3.volume, c_1.volume - c_2.volume)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_cargo_sub_failure_no_item(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		item_dict[i_1] = i_1_qty

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_2] = i_2_qty

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		c_3 = None

		with self.assertRaises(CargoSubtractionError):
			c_3 = c_1 - c_2

		self.assertIsNone(c_3)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_cargo_sub_failure_not_enough_units(self):
		cls = Cargo
		item_dict = dict()

		i = IronBar
		i_qty_1 = 1

		item_dict[i] = i_qty_1

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_qty_2 = 2

		item_dict[i] = i_qty_2

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		c_3 = None

		with self.assertRaises(CargoSubtractionError):
			c_3 = c_1 - c_2

		self.assertIsNone(c_3)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_cargo_isub_success(self):
		cls = Cargo
		item_dict = dict()

		i = IronBar
		i_qty_1 = 2

		item_dict[i] = i_qty_1

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_qty_2 = 1

		item_dict[i] = i_qty_2

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		c_1 -= c_2

		self.assertIsNotNone(c_1)
		self.assertFalse(c_1.is_empty)
		self.assertIsNot(c_1.item_dict, c_2.item_dict)
		self.assertTrue(i in c_1.item_dict)

		self.assertEqual(c_1.mass, i.mass * i_qty_1 - i.mass * i_qty_2)
		self.assertEqual(c_1.volume, i.volume * i_qty_1 - i.volume * i_qty_2)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_cargo_isub_failure_no_item(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		item_dict[i_1] = i_1_qty

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_2] = i_2_qty

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		with self.assertRaises(CargoSubtractionError):
			c_1 -= c_2

		self.assertIsNotNone(c_1)
		self.assertFalse(c_1.is_empty)
		self.assertIsNot(c_1.item_dict, c_2.item_dict)
		self.assertTrue(i_1 in c_1.item_dict)
		self.assertEqual(c_1.item_dict[i_1], i_1_qty)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_cargo_isub_failure_not_enough_units(self):
		cls = Cargo
		item_dict = dict()

		i = IronBar
		i_qty_1 = 1

		item_dict[i] = i_qty_1

		c_1 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_qty_2 = 2

		item_dict[i] = i_qty_2

		c_2 = cls(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		c_3 = None

		with self.assertRaises(CargoSubtractionError):
			c_1 -= c_2

		self.assertIsNotNone(c_1)
		self.assertFalse(c_1.is_empty)
		self.assertIsNot(c_1.item_dict, c_2.item_dict)
		self.assertTrue(i in c_1.item_dict)
		self.assertEqual(c_1.item_dict[i], i_qty_1)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_cargo_get_all_by_class(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)

		items = c.get_all_by_class(Goods)
		self.assertIsNotNone(items)
		self.assertEqual(len(items), 1)
		self.assertTrue(i_1 in items)
		self.assertEqual(items[i_1], i_1_qty)

		items = c.get_all_by_class(Ore)
		self.assertIsNotNone(items)
		self.assertEqual(len(items), 1)
		self.assertTrue(i_2 in items)
		self.assertEqual(items[i_2], i_2_qty)

		items = c.get_all_by_class(Gas)
		self.assertIsNotNone(items)
		self.assertEqual(len(items), 0)

	def test_cargo_mass(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)
		self.assertFalse(c.is_empty)

		self.assertEqual(c.mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty)
		self.assertNotEqual(c.mass, 0)

		c.item_dict = dict()

		self.assertNotEqual(c.mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty)
		self.assertEqual(c.mass, 0)

		self.assertEqual(len(Entity.entity_list), 1)

	def test_cargo_volume(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)
		self.assertFalse(c.is_empty)

		self.assertEqual(c.volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty)
		self.assertNotEqual(c.volume, 0)

		c.item_dict = dict()

		self.assertNotEqual(c.volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty)
		self.assertEqual(c.volume, 0)

		self.assertEqual(len(Entity.entity_list), 1)

	def test_cargo_is_empty(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)
		self.assertEqual(c.is_empty, not bool(len(c.item_dict)))
		self.assertFalse(c.is_empty)

		c.item_dict = dict()

		self.assertEqual(c.is_empty, not bool(len(c.item_dict)))
		self.assertTrue(c.is_empty)

		self.assertEqual(len(Entity.entity_list), 1)

	def test_cargo_get_total_mass_by_class(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)

		items_mass = c.get_total_mass_by_class(Goods)
		self.assertIsNotNone(items_mass)
		self.assertEqual(items_mass, i_1.mass * i_1_qty)

		items_mass = c.get_total_mass_by_class(Ore)
		self.assertIsNotNone(items_mass)
		self.assertEqual(items_mass, i_2.mass * i_2_qty)

		items_mass = c.get_total_mass_by_class(Gas)
		self.assertIsNotNone(items_mass)
		self.assertEqual(items_mass, 0)

	def test_cargo_get_total_volume_by_class(self):
		cls = Cargo
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)

		items_volume = c.get_total_volume_by_class(Goods)
		self.assertIsNotNone(items_volume)
		self.assertEqual(items_volume, i_1.volume * i_1_qty)

		items_volume = c.get_total_volume_by_class(Ore)
		self.assertIsNotNone(items_volume)
		self.assertEqual(items_volume, i_2.volume * i_2_qty)

		items_volume = c.get_total_volume_by_class(Gas)
		self.assertIsNotNone(items_volume)
		self.assertEqual(items_volume, 0)


class StorageTest(NoNameTestCase):

	def test_storage_class_init(self):
		cls = Storage

		self.assertIsNotNone(cls)

		self.assertIsNotNone(cls.attributes_dict)
		self.assertIsInstance(cls.attributes_dict, dict)
		self.assertGreater(len(cls.attributes_dict), 0)

		self.assertSetEqual(set(cls.attributes_dict.keys()), {
			'name',
			'parent_env',
			'stored_cargo',
			'capacity',
			'reserved_cargo_list',
			'expected_cargo_list'
		})
		self.assertIsNotNone(cls.attributes_dict['name'])
		self.assertIsNotNone(cls.attributes_dict['parent_env'])
		self.assertIsNotNone(cls.attributes_dict['stored_cargo'])
		self.assertIsNotNone(cls.attributes_dict['capacity'])
		self.assertIsNotNone(cls.attributes_dict['reserved_cargo_list'])
		self.assertIsNotNone(cls.attributes_dict['expected_cargo_list'])

		for k, v in cls.attributes_dict.items():
			self.assertIsInstance(v, tuple)
			self.assertEqual(len(v), 2)
			self.assertIsInstance(v[0], type(lambda x: x))

		self.assertEqual(cls.base_name, 'Storage')

	def test_storage_init_empty(self):
		cls = Storage
		s = cls()
		self.assertIsNotNone(s)

		self.assertIsNotNone(s.capacity)
		self.assertIsInstance(s.capacity, dict)
		self.assertEqual(len(s.capacity), 3)
		self.assertDictEqual(s.capacity, {Goods: 0.0, Ore: 0.0, Gas: 0.0})

		self.assertIsNotNone(s.stored_cargo)
		self.assertIsInstance(s.stored_cargo, Cargo)
		self.assertIsInstance(Storage.attributes_dict['stored_cargo'][1], Cargo)
		self.assertIsNot(s.stored_cargo, Storage.attributes_dict['stored_cargo'][1])
		self.assertTrue(s.is_empty)

		self.assertIsNotNone(s.reserved_cargo_list)
		self.assertIsInstance(s.reserved_cargo_list, list)
		self.assertEqual(len(s.reserved_cargo_list), 0)

		self.assertIsNotNone(s.expected_cargo_list)
		self.assertIsInstance(s.expected_cargo_list, list)
		self.assertEqual(len(s.expected_cargo_list), 0)

		self.assertIsNot(s.reserved_cargo_list, s.expected_cargo_list)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_storage_init_with_attributes(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 2000, Ore: 5000, Gas: 0}

		e = Entity()

		s = cls(capacity=capacity, stored_cargo=c, parent_env=e)

		self.assertIsNotNone(s)

		self.assertIsNotNone(s.capacity)
		self.assertIsInstance(s.capacity, dict)
		self.assertEqual(len(s.capacity), 3)
		self.assertDictEqual(s.capacity, capacity)

		self.assertIsNotNone(s.stored_cargo)
		self.assertIsInstance(s.stored_cargo, Cargo)
		self.assertIsInstance(Storage.attributes_dict['stored_cargo'][1], Cargo)
		self.assertIsNot(s.stored_cargo, Storage.attributes_dict['stored_cargo'][1])
		self.assertIsNot(s.stored_cargo, c)
		self.assertTrue(s.is_empty)

		self.assertIsNotNone(s.parent_env)
		self.assertIs(s.parent_env, e)

		self.assertEqual(len(Entity.entity_list), 4)

	def test_storage_expect_cargo_success(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		res = s.expect_cargo(c)

		self.assertTrue(res)
		self.assertIsNotNone(s.expected_cargo_list)
		self.assertIsInstance(s.expected_cargo_list, list)
		self.assertEqual(len(s.expected_cargo_list), 1)
		self.assertIs(s.expected_cargo_list[0], c)
		self.assertIs(s.expected_cargo_list[0].parent_env, s)

		self.assertTrue(i_1 in s.expected_cargo_list[0].item_dict)
		self.assertTrue(i_2 in s.expected_cargo_list[0].item_dict)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_storage_expect_cargo_failure(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1500

		i_2 = IronOre
		i_2_qty = 250

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 1, Ore: 1, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertLessEqual(capacity[item_type], c.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		res = False

		with self.assertRaises(NotEnoughSpaceError):
			res = s.expect_cargo(c)

		self.assertFalse(res)
		self.assertIsNotNone(s.expected_cargo_list)
		self.assertIsInstance(s.expected_cargo_list, list)
		self.assertEqual(len(s.expected_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_storage_release_expected_cargo_success(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c)
		res = s.release_expected_cargo(c)

		self.assertTrue(res)
		self.assertIsNotNone(s.expected_cargo_list)
		self.assertIsInstance(s.expected_cargo_list, list)
		self.assertEqual(len(s.expected_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_storage_release_expected_cargo_failure(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		item_dict[i_1] = i_1_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_2] = i_2_qty

		c_2 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		res = False

		s.expect_cargo(c_1)

		with self.assertRaises(CanNotReleaseCargoError):
			res = s.release_expected_cargo(c_2)

		self.assertFalse(res)
		self.assertIsNotNone(s.expected_cargo_list)
		self.assertIsInstance(s.expected_cargo_list, list)
		self.assertEqual(len(s.expected_cargo_list), 1)
		self.assertIs(s.expected_cargo_list[0], c_1)

		self.assertEqual(len(Entity.entity_list), 4)

	def test_storage_store_cargo_success(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c)
		res = s.store_cargo(c)

		self.assertTrue(res)
		self.assertIsNotNone(s.stored_cargo)
		self.assertIsInstance(s.stored_cargo, Cargo)
		self.assertIsNot(s.stored_cargo, c)
		self.assertIs(s.stored_cargo.parent_env, s)

		self.assertTrue(i_1 in s.stored_cargo.item_dict)
		self.assertEqual(s.stored_cargo.item_dict[i_1], i_1_qty)
		self.assertTrue(i_2 in s.stored_cargo.item_dict)
		self.assertEqual(s.stored_cargo.item_dict[i_2], i_2_qty)

		self.assertIsNotNone(s.expected_cargo_list)
		self.assertIsInstance(s.expected_cargo_list, list)
		self.assertEqual(len(s.expected_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_storage_store_cargo_failure(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		res = False

		with self.assertRaises(CargoNotExpectedError):
			res = s.store_cargo(c)

		self.assertFalse(res)
		self.assertIsNotNone(s.stored_cargo)
		self.assertEqual(len(s.stored_cargo.item_dict), 0)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_storage_reserve_cargo_success(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c_1.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c_1)
		s.store_cargo(c_1)

		self.assertFalse(s.is_empty)

		i_3 = IronOre
		i_3_qty = 1

		item_dict = dict()
		item_dict[i_3] = i_3_qty

		c_2 = Cargo(item_dict=item_dict)

		res = s.reserve_cargo(c_2)

		self.assertTrue(res)
		self.assertIsNotNone(s.reserved_cargo_list)
		self.assertIsInstance(s.reserved_cargo_list, list)
		self.assertEqual(len(s.reserved_cargo_list), 1)
		self.assertIs(s.reserved_cargo_list[0], c_2)
		self.assertIs(s.reserved_cargo_list[0].parent_env, s)
		self.assertIsNot(s.reserved_cargo_list[0], c_1)

		self.assertTrue(i_3 in s.reserved_cargo_list[0].item_dict)
		self.assertEqual(s.reserved_cargo_list[0].item_dict[i_3], i_3_qty)

		self.assertEqual(len(Entity.entity_list), 5)

	def test_storage_reserve_cargo_failure(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c_1.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c_1)
		s.store_cargo(c_1)

		self.assertFalse(s.is_empty)

		i_3 = IronOre
		i_3_qty = 3

		item_dict = dict()
		item_dict[i_3] = i_3_qty

		c_2 = Cargo(item_dict=item_dict)

		res = False

		with self.assertRaises(CanNotReserveCargoError):
			res = s.reserve_cargo(c_2)

		self.assertFalse(res)
		self.assertIsNotNone(s.reserved_cargo_list)
		self.assertIsInstance(s.reserved_cargo_list, list)
		self.assertEqual(len(s.reserved_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 4)

	def test_storage_release_reserved_cargo_success(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c_1.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c_1)
		s.store_cargo(c_1)

		self.assertFalse(s.is_empty)

		i_3 = IronOre
		i_3_qty = 1

		item_dict = dict()
		item_dict[i_3] = i_3_qty

		c_2 = Cargo(item_dict=item_dict)

		s.reserve_cargo(c_2)
		res = s.release_reserve_cargo(c_2)

		self.assertTrue(res)
		self.assertIsNotNone(s.reserved_cargo_list)
		self.assertIsInstance(s.reserved_cargo_list, list)
		self.assertEqual(len(s.reserved_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 5)

	def test_storage_release_reserved_cargo_failure(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c_1.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c_1)
		s.store_cargo(c_1)

		self.assertFalse(s.is_empty)

		i_3 = IronOre
		i_3_qty = 1

		item_dict = dict()
		item_dict[i_3] = i_3_qty

		c_2 = Cargo(item_dict=item_dict)

		res = False

		with self.assertRaises(CanNotReleaseCargoError):
			res = s.release_reserve_cargo(c_2)

		self.assertFalse(res)
		self.assertIsNotNone(s.reserved_cargo_list)
		self.assertIsInstance(s.reserved_cargo_list, list)
		self.assertEqual(len(s.reserved_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_storage_transfer_cargo_success(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c_1.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c_1)
		s.store_cargo(c_1)

		self.assertFalse(s.is_empty)

		i_3 = IronOre
		i_3_qty = 1

		item_dict = dict()
		item_dict[i_3] = i_3_qty

		c_2 = Cargo(item_dict=item_dict)

		s.reserve_cargo(c_2)
		res = s.transfer_cargo(c_2)

		self.assertTrue(res)

		self.assertEqual(s.stored_cargo.mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty - i_3.mass * i_3_qty)
		self.assertEqual(s.stored_cargo.volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty - i_3.volume * i_3_qty)

		self.assertIsNotNone(s.reserved_cargo_list)
		self.assertIsInstance(s.reserved_cargo_list, list)
		self.assertEqual(len(s.reserved_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 5)

	def test_storage_transfer_cargo_failure(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		capacity = {Goods: 200, Ore: 500, Gas: 0}

		for item_type in (Goods, Ore, Gas):
			self.assertGreaterEqual(capacity[item_type], c_1.get_total_volume_by_class(item_type))

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)

		s.expect_cargo(c_1)
		s.store_cargo(c_1)

		self.assertFalse(s.is_empty)

		i_3 = IronOre
		i_3_qty = 1

		item_dict = dict()
		item_dict[i_3] = i_3_qty

		c_2 = Cargo(item_dict=item_dict)

		res = False

		with self.assertRaises(CargoNotReservedError):
			res = s.transfer_cargo(c_2)

		self.assertFalse(res)

		self.assertEqual(s.stored_cargo.mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty)
		self.assertEqual(s.stored_cargo.volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty)

		self.assertIsNotNone(s.reserved_cargo_list)
		self.assertIsInstance(s.reserved_cargo_list, list)
		self.assertEqual(len(s.reserved_cargo_list), 0)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_storage_total_stored_mass(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 2000, Ore: 5000, Gas: 0}

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)
		self.assertTrue(s.is_empty)

		s.expect_cargo(c)
		s.store_cargo(c)

		self.assertIsNotNone(s.stored_cargo)
		self.assertIsNot(s.stored_cargo, c)
		self.assertFalse(s.is_empty)
		self.assertIs(s.stored_cargo.parent_env, s)

		self.assertEqual(s.total_stored_mass, c.mass)
		self.assertEqual(s.total_stored_mass, i_1.mass * i_1_qty + i_2.mass * i_2_qty)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_storage_total_stored_volume(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 2000, Ore: 5000, Gas: 0}

		s = cls(capacity=capacity)

		self.assertIsNotNone(s)
		self.assertTrue(s.is_empty)

		s.expect_cargo(c)
		s.store_cargo(c)

		self.assertIsNotNone(s.stored_cargo)
		self.assertIsNot(s.stored_cargo, c)
		self.assertFalse(s.is_empty)
		self.assertIs(s.stored_cargo.parent_env, s)

		self.assertEqual(s.total_stored_volume, c.volume)
		self.assertEqual(s.total_stored_volume, i_1.volume * i_1_qty + i_2.volume * i_2_qty)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_storage_get_filled_space_by_class(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 2000, Ore: 5000, Gas: 0}

		s = cls(capacity=capacity)

		s.expect_cargo(c)
		s.store_cargo(c)

		self.assertIsNotNone(s)

		self.assertIsNotNone(s.stored_cargo)
		self.assertIsNot(s.stored_cargo, c)
		self.assertFalse(s.is_empty)

		filled_space = s.get_filled_space_by_class(Goods)
		self.assertIsNotNone(filled_space)
		self.assertEqual(filled_space, i_1.volume * i_1_qty)
		self.assertEqual(filled_space, c.get_total_volume_by_class(Goods))

		filled_space = s.get_filled_space_by_class(Ore)
		self.assertIsNotNone(filled_space)
		self.assertEqual(filled_space, i_2.volume * i_2_qty)
		self.assertEqual(filled_space, c.get_total_volume_by_class(Ore))

		filled_space = s.get_filled_space_by_class(Gas)
		self.assertIsNotNone(filled_space)
		self.assertEqual(filled_space, 0)

		self.assertEqual(len(Entity.entity_list), 2)

	def test_storage_get_reserved_space_by_class(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_1] = i_1_qty
		item_dict[i_2] = i_2_qty

		c = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c)

		capacity = {Goods: 2000, Ore: 5000, Gas: 0}

		s = cls(capacity=capacity)

		s.expect_cargo(c)

		self.assertIsNotNone(s)

		self.assertIsNotNone(s.expected_cargo_list)
		self.assertEqual(len(s.expected_cargo_list), 1)
		self.assertIs(s.expected_cargo_list[0], c)
		self.assertTrue(s.is_empty)

		reserved_space = s.get_reserved_space_by_class(Goods)
		self.assertIsNotNone(reserved_space)
		self.assertEqual(reserved_space, i_1.volume * i_1_qty)
		self.assertEqual(reserved_space, c.get_total_volume_by_class(Goods))

		reserved_space = s.get_reserved_space_by_class(Ore)
		self.assertIsNotNone(reserved_space)
		self.assertEqual(reserved_space, i_2.volume * i_2_qty)
		self.assertEqual(reserved_space, c.get_total_volume_by_class(Ore))

		reserved_space = s.get_reserved_space_by_class(Gas)
		self.assertIsNotNone(reserved_space)
		self.assertEqual(reserved_space, 0)

		self.assertEqual(len(Entity.entity_list), 3)

	def test_storage_get_occupied_space_by_class(self):
		cls = Storage
		item_dict = dict()

		i_1 = IronBar
		i_1_qty = 1

		item_dict[i_1] = i_1_qty

		c_1 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_1)

		item_dict = dict()

		i_2 = IronOre
		i_2_qty = 2

		item_dict[i_2] = i_2_qty

		c_2 = Cargo(item_dict=item_dict)

		self.assertIsNotNone(c_2)

		capacity = {Goods: 2000, Ore: 5000, Gas: 0}

		s = cls(capacity=capacity)

		s.expect_cargo(c_1)
		s.store_cargo(c_1)

		s.expect_cargo(c_2)

		self.assertIsNotNone(s)

		self.assertIsNotNone(s.stored_cargo)
		self.assertIsNot(s.stored_cargo, c_1)
		self.assertFalse(s.is_empty)
		self.assertTrue(i_1 in s.stored_cargo.item_dict)
		self.assertEqual(s.stored_cargo.item_dict[i_1], i_1_qty)

		self.assertIsNotNone(s.expected_cargo_list)
		self.assertEqual(len(s.expected_cargo_list), 1)
		self.assertIs(s.expected_cargo_list[0], c_2)

		occupied_space = s.get_occupied_space_by_class(Goods)
		self.assertIsNotNone(occupied_space)
		self.assertEqual(occupied_space, i_1.volume * i_1_qty)
		self.assertEqual(occupied_space, c_1.get_total_volume_by_class(Goods))
		self.assertEqual(occupied_space, s.get_filled_space_by_class(Goods))

		occupied_space = s.get_reserved_space_by_class(Ore)
		self.assertIsNotNone(occupied_space)
		self.assertEqual(occupied_space, i_2.volume * i_2_qty)
		self.assertEqual(occupied_space, c_2.get_total_volume_by_class(Ore))
		self.assertEqual(occupied_space, s.get_reserved_space_by_class(Ore))

		occupied_space = s.get_reserved_space_by_class(Gas)
		self.assertIsNotNone(occupied_space)
		self.assertEqual(occupied_space, 0)

		self.assertEqual(len(Entity.entity_list), 3)


if __name__ == '__main__':
	main()
