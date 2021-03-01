from com.nng.entity.entity import Entity
from com.nng.position import Vector3
from com.nng.entity.building import Excavator, Warehouse
from com.nng.entity.vehicle import MuleMKI
from com.nng.entity.cargo import Cargo
from com.nng.entity.item import IronOre
import logging
from pyglet.window import key, mouse, Window
from pyglet.graphics import Batch
from pyglet import clock, app
from pyglet.gl import *

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s')


# miner = Excavator(pos=Vector3(0.0, 0.0, 0.0))
# warehouse = Warehouse(pos=Vector3(10.0, 0.0, 0.0))
# vehicle = MuleMKI(pos=Vector3(5.0, 0.0, 0.0))
# cargo = Cargo(item_dict={IronOre: 100})
#
# miner.storage.expect_cargo(cargo)
# miner.storage.store_cargo(cargo)


w = 1920
h = 1080

config = Config(sample_buffers=1, samples=8)
window = Window(width=w, height=h, config=config)
cycle = 0

batch = Batch()


vertex_list = batch.add(
	4,
	gl.GL_QUADS,
	None,
	('v2f', (
		w/2 - 50, h/2 - 50,
		w/2 + 50, h/2 - 50,
		w/2 + 50, h/2 + 50,
		w/2 - 50, h/2 + 50
	)),
	('c3B', (255, 0, 0) * 4)
)


@window.event
def on_draw():
	global batch
	window.clear()
	# batch.draw()


def game_update(dt):
	global cycle, batch
	cycle += 1
	# vertex_list.colors = list(rand_color() + rand_color() + rand_color() + rand_color())
	# vertex_list.vertices = [
	# 	100+int(50*sin(cycle/3)),
	# 	100+int(50*cos(cycle/3)),
	#
	# 	200+int(50*sin(cycle/3)),
	# 	100+int(50*cos(cycle/3)),
	#
	# 	200+int(50*sin(cycle/3)),
	# 	200+int(50*cos(cycle/3)),
	#
	# 	100+int(50*sin(cycle/3)),
	# 	200+int(50*cos(cycle/3))
	# ]
	print(f"[{cycle}]", end='\n\n')
	Entity.print_all()
	Entity.update_all()

	print(('-' * 50 + '\n') * 3, end='')


clock.schedule_interval(game_update, 1/1.0)


@window.event
def on_mouse_motion(x, y, dx, dy):
	pass


@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		pass


@window.event
def on_mouse_release(x, y, button, modifiers):
	pass


@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.SPACE:
		pass


app.run()
