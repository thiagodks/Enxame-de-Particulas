import random

class Particle:

	def __init__(self, ndim=4, xmin=-3, xmax=3):
		self.fitness = None
		self.ndim = ndim
		self.xmin = xmin
		self.xmax = xmax
		self.speed = [0] * ndim
		self.g_best = None
		self.coord = self.__initial_coord()
		self.p_best = self.coord.copy()
		self.neighbors = []

	def __initial_coord(self):
		return [random.uniform(self.xmin, self.xmax) for _ in range(self.ndim)]

	def set_neighbors(self, possible_neighbors, neighborhood="general"):
		def general_neighbor(possible_neighbors):
			return possible_neighbors
		def two_neighbor(possible_neighbors):
			return possible_neighbors

		if neighborhood == "general":
			self.neighbors = general_neighbor(possible_neighbors)
		elif neighborhood == "two":
			self.neighbors = two_neighbor(possible_neighbors)

		len_n = len(self.neighbors)
		for i in range(0, len_n):
			self.neighbors[i].update_fitness()
		
		self.update_gbest()
	
	def update_gbest(self):
		best_particle = min(self.neighbors, key=lambda x: x.fitness)
		if self.g_best == None:
			self.g_best = best_particle.coord
		elif best_particle.fitness < self.calc_fitness(self.g_best):
			self.g_best = best_particle.coord

	def update_fitness(self):
		self.fitness = self.__colville(self.coord)

	def calc_fitness(self, coord):
		return self.__colville(coord)

	def __colville(self, coord):
		x1, x2, x3, x4 = coord
		return (100*(x1 - (x2**2))**2 + (1 - x1)**2 + 90*(x4 - x3)**2 + (1 - x3)**2 +
			    10.1*((x2 - 1)**2 + (x4 - 1)**2) + 19.8*(x2 - 1)*(x4 - 1))

	def update_speed(self, W, C1, C2):
		prev_speed = self.speed
		r1, r2 = random.random(), random.random()

		for i in range(0, self.ndim):
			self.speed[i] = ((W * prev_speed[i]) + (C1 * r1 * (self.p_best[i] - self.coord[i])) +
							 (C2 * r2 * (self.g_best[i] - self.coord[i])))

	def update_position(self):
		self.coord = [(self.coord[i] + self.speed[i]) for i in range(0, self.ndim)]
		for i in range(0, self.ndim):
			if self.coord[i] > self.xmax: self.coord[i] = self.xmax
			elif self.coord[i] < self.xmin: self.coord[i] = self.xmin