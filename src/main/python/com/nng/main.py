from time import sleep
from com.nng.entity.entity import Entity
from com.nng.position import Vector3
from com.nng.entity.building import Miner, Warehouse
from com.nng.entity.vehicle import MuleMKI
from com.nng.entity.cargo import Cargo
from com.nng.entity.item import IronOre
import logging

logging.basicConfig(level=logging.WARNING, format='[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s')


def run(sleep_time_sec):

	miner = Miner(pos=Vector3(0.0, 0.0, 0.0))
	warehouse = Warehouse(pos=Vector3(10.0, 0.0, 0.0))
	vehicle = MuleMKI(pos=Vector3(5.0, 0.0, 0.0))
	cargo = Cargo(item_dict={IronOre: 100})

	miner.storage.expect_cargo(cargo)
	miner.storage.store_cargo(cargo)


	for i in range(10):
		print(f"[{i}]", end='\n\n')
		Entity.update_all()
		Entity.print_all()

		print(('-' * 50 + '\n') * 3, end='')

		sleep(sleep_time_sec)

	# tick = 0
	# cmd = '_'
	# while cmd:
	#
	# 	if cmd == '0':
	# 		print("All entities:")
	# 		Entity.print_all()
	#
	# 	print(f"[{tick}] Command={cmd}", end='\n\n')
	# 	print("0 - all entities")
	# 	print("1 - set up Transport task")
	#
	# 	cmd = input(">")
	# 	print(('-'*50 + '\n') * 3, end='')
	# 	tick += 1


run(0.5)
