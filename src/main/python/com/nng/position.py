from math import sqrt, radians, degrees, sin, cos, acos


class Vector3:

	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x, self.y, self.z = round(x, 8), round(y, 8), round(z, 8)

	def __str__(self):
		return f"Vector3({self.x}; {self.y}: {self.z})"

	def __add__(self, other):
		return Vector3(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z
		)

	def __sub__(self, other):
		return Vector3(
			self.x - other.x,
			self.y - other.y,
			self.z - other.z
		)

	def __bool__(self):
		return bool(self.x or self.y or self.z)

	def __neg__(self):
		return Vector3(-self.x, -self.y, -self.z)

	def __abs__(self):
		return sqrt(self.x**2 + self.y**2 + self.z**2)

	def __mul__(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z

	@classmethod
	def dist(cls, v3_1, v3_2):
		return sqrt((v3_1.x - v3_2.x)**2 + (v3_1.y - v3_2.y)**2 + (v3_1.z - v3_2.z)**2)

	def dist_to(self, other):
		return self.dist(self, other)


class Polar3:

	def __init__(self, a_deg=0.0, b_deg=0.0, r=0.0):
		self.a_deg = round(a_deg % 360, 6)
		self.b_deg = round(b_deg % 360, 6)
		self.r = round(r, 6)

	def __str__(self):
		return f"({self.a_deg}; {self.b_deg}; {self.r})"

	def __add__(self, other):
		a_rad = round((self.a_deg * self.r + other.a_deg * other.r) / (self.r + other.r), 6)
		b_rad = round((self.b_deg * self.r + other.b_deg * other.r) / (self.r + other.r), 6)
		r = round(self.r + other.r, 6)
		return Polar3(a_rad, b_rad, r)

	def __bool__(self):
		return bool(self.r)

	def __neg__(self):
		return Polar3(self.a_deg + 180, self.b_deg + 180, self.r)

	def to_cartesian(self):
		return Vector3(
			self.r * sin(radians(self.a_deg)) * cos(radians(self.b_deg)),
			self.r * sin(radians(self.a_deg)) * sin(radians(self.b_deg)),
			self.r * cos(radians(self.a_deg))
		)

	@classmethod
	def from_cartesian(cls, vec3=Vector3()):
		r = abs(vec3)
		a_deg = degrees(acos(vec3.x / sqrt(vec3.x**2 + vec3.y**2)))
		b_deg = degrees(acos(vec3.z / r))
		return cls(a_deg, b_deg, r)
