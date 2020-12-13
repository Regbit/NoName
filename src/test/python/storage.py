from unittest import TestCase, main, skip
from src.main.python.entity.item import *
from src.main.python.entity.storage import *


class CargoTest(TestCase):

	def tearDown(self) -> None:
		Entity.entity_list.clear()

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

	def test_cargo_init_empty(self):
		cls = Cargo
		c = cls()
		self.assertIsNotNone(c)

		self.assertIsNotNone(c.item_dict)
		self.assertIsInstance(c.item_dict, dict)

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
		i_2 = IronOre

		item_dict[i_1] = 1
		item_dict[i_2] = 2

		c = cls(item_dict=item_dict)

		self.assertIsNotNone(c)
		self.assertEqual(c.item_dict, item_dict)
		self.assertTrue(i_1 in c.item_dict)
		self.assertTrue(i_2 in c.item_dict)


@skip
class StorageTest(TestCase):

	def tearDown(self) -> None:
		Entity.entity_list.clear()


if __name__ == '__main__':
	main()
