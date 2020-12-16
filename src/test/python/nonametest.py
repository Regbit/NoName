from unittest import TestCase
from entity.entity import Entity
import logging


# logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s')


class NoNameTestCase(TestCase):

	log = logging.getLogger(__name__)

	@classmethod
	def clear(cls):
		Entity.entity_list.clear()
		cls.log.info(f"[{cls.__name__}] Entity.entity_list has been cleared")

	def setUp(self) -> None:
		self.clear()

	def tearDown(self) -> None:
		self.clear()
