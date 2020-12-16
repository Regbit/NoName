from time import sleep
from src.main.python.com.nng.entity.entity import Entity
from src.main.python.com.nng.position import Vector3
from src.main.python.com.nng.entity.building import Miner, Warehouse
from src.main.python.com.nng.entity.vehicle import ScavengerMKI
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s')


def run(sleep_time_sec):

	miner = Miner(pos=Vector3(0.0, 0.0, 0.0))
	warehouse = Warehouse(pos=Vector3(10.0, 0.0, 0.0))
	transport = ScavengerMKI(pos=Vector3(5.0, 0.0, 0.0))

	tick = 0
	cmd = input(">")
	while cmd:
		print("0 - all entities")

		print(f"Command={cmd}")
		if cmd == '0':
			print("All entities:")
			for e in Entity.entity_list:
				print(e)

		print(('-'*50 + '\n') * 3)
		print(f"[{tick}]")
		cmd = input(">")
		tick += 1



run(1)
