from unittest import main, skip
from src.test.python.nonametest import NoNameTestCase
import logging


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s')


class TaskTest(NoNameTestCase):

	def test_transport_task(self):
		pass


if __name__ == '__main__':
	main()
