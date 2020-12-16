from com.nng.entity.entity import Entity


class CargoSubtractionError(Exception):
	pass


class Cargo(Entity):
	"""
	Class used to represent and manage cargo - a set of items.
	Cargo is created when two Entities interact (item transfer)
	"""
	attributes_dict = Entity.attributes_dict_copy()
	attributes_dict['item_dict'] = lambda x: isinstance(x, dict) and len(x), dict()
	base_name = 'Cargo'

	def __init__(self, **kwargs):
		"""

		:param kwargs: {
			name: str,
			parent_env: Entity,
			item_dict: dict(Item(cls), float)
		}
		"""

		self.item_dict: dict = None
		super().__init__(**kwargs)

	def __str__(self):
		items = '\n\t'.join([str(k.cls_name()) + f"; Q={v}" for k, v in self.item_dict.items()])
		return f"{self.obj_info}" + (f":\n\t{items}" if len(self.item_dict) else "")

	def add(self, other):
		new_item_dict = dict()
		for k in list(self.item_dict.keys()) + list(other.item_dict.keys()):
			new_item_dict[k] = (self.item_dict.get(k) or 0) + (other.item_dict.get(k) or 0)
		return new_item_dict

	def __add__(self, other):
		return Cargo(item_dict=self.add(other))

	def __iadd__(self, other):
		self.item_dict.update(self.add(other))
		return self

	def sub(self, other):
		for k in other.item_dict.keys():
			if k not in self.item_dict:
				raise CargoSubtractionError(f"Instance '{self.obj_info_short}' does not have item {k.cls_name()} to subtract from!")
			elif self.item_dict[k] < other.item_dict[k]:
				raise CargoSubtractionError(f"Instance '{self.obj_info_short}' does not have {other.item_dict[k]} units of item {k} to subtract from!")

		new_item_dict = dict()
		for k in self.item_dict.keys():
			diff = self.item_dict.get(k) - (other.item_dict.get(k) or 0)
			if diff:
				new_item_dict[k] = diff

		return new_item_dict

	def __sub__(self, other):
		out = None

		try:
			out = Cargo(item_dict=self.sub(other))
		except CargoSubtractionError as err:
			raise err

		return out

	def __isub__(self, other):
		try:
			self.item_dict.update(self.sub(other))
		except CargoSubtractionError as err:
			raise err

		return self

	def __bool__(self):
		return bool(sum(self.item_dict.values()) or 0)

	@property
	def mass(self) -> float:
		return sum(item.mass * qty for item, qty in self.item_dict.items())

	@property
	def volume(self) -> float:
		return sum(item.volume * qty for item, qty in self.item_dict.items())

	@property
	def is_empty(self) -> bool:
		return not bool(len(self.item_dict))

	def has_item(self, item_class) -> bool:
		return item_class in self.item_dict

	def get_all_by_class(self, cls) -> dict:
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return {k: v for k, v in self.item_dict.items() if issubclass(k, cls)}

	def get_total_mass_by_class(self, cls) -> float:
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return sum([k.mass * v for k, v in self.item_dict.items() if issubclass(k, cls)])

	def get_total_volume_by_class(self, cls) -> float:
		"""

		:param cls: Goods, Ore or Gas
		:return:
		"""
		return sum([k.volume * v for k, v in self.item_dict.items() if issubclass(k, cls)])

	def update(self):
		pass
