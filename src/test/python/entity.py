from unittest import TestCase, main, skip
from src.main.python.entity.entity import *
import gc


class EntityTest(TestCase):

	def tearDown(self) -> None:
		Entity.entity_list.clear()

	def test_entity_class_init(self):
		cls = Entity

		self.assertIsNotNone(cls)

		self.assertIsNotNone(cls.entity_list)
		self.assertIsInstance(cls.entity_list, list)
		self.assertEqual(len(cls.entity_list), 0)

		self.assertIsNotNone(cls.attributes_dict)
		self.assertIsInstance(cls.attributes_dict, dict)
		self.assertGreater(len(cls.attributes_dict), 0)

		self.assertEqual(set(cls.attributes_dict.keys()), {'name', 'parent_env'})
		self.assertIsNotNone(cls.attributes_dict['name'])
		self.assertIsNotNone(cls.attributes_dict['parent_env'])

		for k, v in cls.attributes_dict.items():
			self.assertIsInstance(v, tuple)
			self.assertEqual(len(v), 2)
			self.assertIsInstance(v[0], type(lambda x: x))

		self.assertEqual(cls.base_name, 'Entity')

	def test_entity_init(self):
		cls = Entity
		e = Entity()
		self.assertIsNotNone(e)

		self.assertIsNone(e.name)
		self.assertIsNone(e.parent_env)

		self.assertIsNotNone(e)
		self.assertEqual(len(cls.entity_list), 1)

	def test_entity_init_with_attributes(self):
		name = 'Entity'
		parent_env = Entity()

		e = Entity(name=name, parent_env=parent_env)
		self.assertIsNotNone(e)

		self.assertEqual(e.name, name)
		self.assertEqual(e.parent_env, parent_env)

	def test_entity_init_with_faulty_attributes(self):
		name = 123
		parent_env = 'name'
		e = Entity(name=name, parent_env=parent_env)

		self.assertIsNotNone(e)
		self.assertIsNot(e.name, name)
		self.assertIsNot(e.parent_env, parent_env)

		self.assertEqual(len(Entity.entity_list), 0)

	def test_entity_init_with_nonexistent_attributes(self):
		name = 'Entity'
		parent_env = Entity()
		nonexistent_attribute = 1

		e = Entity(name=name, parent_env=parent_env, nonexistent_attribute=nonexistent_attribute)
		self.assertIsNotNone(e)

		self.assertEqual(e.name, name)
		self.assertEqual(e.parent_env, parent_env)

		with self.assertRaises(AttributeError):
			e.nonexistent_attribute

	def test_entity_attributes_dict_copy(self):
		cls = Entity
		attributes_dict_copy = cls.attributes_dict_copy()
		self.assertIsNotNone(attributes_dict_copy)
		self.assertIsNot(attributes_dict_copy, cls.attributes_dict)
		self.assertEqual(len(attributes_dict_copy), len(cls.attributes_dict))

		for k, v in attributes_dict_copy.items():
			self.assertEqual(v, cls.attributes_dict[k])

	def test_entity_delete_one(self):
		cls = Entity
		e = cls()

		self.assertIsNotNone(e)
		self.assertEqual(len(cls.entity_list), 1)

		cls.delete(e)

		self.assertEqual(len(cls.entity_list), 0)

		gc.collect()
		self.assertEqual(len(gc.get_referrers(e)), 0)

	def test_entity_delete_multiple(self):
		cls = Entity
		e_1 = cls()
		e_2 = cls()
		e_3 = cls()

		self.assertIsNotNone(e_1)
		self.assertIsNotNone(e_2)
		self.assertIsNotNone(e_3)

		self.assertIsNot(e_1, e_2)
		self.assertIsNot(e_1, e_3)
		self.assertIsNot(e_2, e_3)

		self.assertEqual(len(cls.entity_list), 3)

		cls.delete(e_1, e_2)

		self.assertEqual(len(cls.entity_list), 1)

		gc.collect()
		self.assertEqual(len(gc.get_referrers(e_1)), 0)
		self.assertEqual(len(gc.get_referrers(e_2)), 0)

		self.assertIs(cls.entity_list[0], e_3)

	@skip
	def _test_entity_delete_parent(self):
		cls = Entity
		e_par = cls()
		e_ch = cls(parent_env=e_par)

		self.assertIsNotNone(e_par)
		self.assertIsNotNone(e_ch)
		self.assertIsNot(e_par, e_ch)
		self.assertIs(e_ch.parent_env, e_par)
		self.assertEqual(len(cls.entity_list), 2)

		cls.delete(e_par)

		self.assertEqual(len(cls.entity_list), 1)

		gc.collect()
		print("\n"+"!"*25)
		print(gc.get_referrers(e_par))
		print("!"*25)
		# self.assertEqual(len(gc.get_referrers(e_par)), 0)


class MassedEntityTest(TestCase):

	def tearDown(self) -> None:
		Entity.entity_list.clear()

	def test_massed_entity_class_init(self):
		cls = MassedEntity

		self.assertIsNotNone(cls)
		self.assertTrue(issubclass(cls, Entity))

		self.assertIsNotNone(cls.entity_list)
		self.assertIsInstance(cls.entity_list, list)
		self.assertEqual(len(cls.entity_list), 0)
		self.assertIs(cls.entity_list, Entity.entity_list)

		self.assertIsNotNone(cls.attributes_dict)
		self.assertIsInstance(cls.attributes_dict, dict)
		self.assertGreater(len(cls.attributes_dict), 0)

		self.assertEqual(set(cls.attributes_dict.keys()), {'name', 'parent_env'})
		self.assertIsNotNone(cls.attributes_dict['name'])
		self.assertIsNotNone(cls.attributes_dict['parent_env'])

		for k, v in cls.attributes_dict.items():
			self.assertIsInstance(v, tuple)
			self.assertEqual(len(v), 2)
			self.assertIsInstance(v[0], type(lambda x: x))

		self.assertIsNotNone(cls.mass)
		self.assertIsNotNone(cls.volume)


if __name__ == '__main__':
	main()
