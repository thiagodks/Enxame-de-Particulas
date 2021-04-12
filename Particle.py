import random

class Particle:

	def __init__(self, ndim=4, xmin=-3, xmax=3):
		self.fitness = None
		self.ndim = ndim
		self.xmin = xmin
		self.xmax = xmax
		self.speed = [0] * ndim
		self.p_best = [0] * ndim
		self.g_best = [0] * ndim
		self.coord = self.__initial_coord()
		
	def __initial_coord(self):
		return [random.uniform(self.xmin, self.xmax) for _ in range(self.ndim)]

	def calc_fitness(self):
		self.fitness = self.__colville()

	def __colville(self):
		x1, x2, x3, x4 = self.coord
		return (100*(x1 - (x2**2))**2 + (1 - x1)**2 + 90*(x4 - x3)**2 + (1 - x3)**2 +
			    10.1*((x2 - 1)**2 + (x4 - 1)**2) + 19.8*(x2 - 1)*(x4 - 1))

	def update_speed(self, W, C1, C2):
		prev_speed = self.speed[-1]
		r1, r2 = random.random(), random.random()

		for i in range(0, self.ndim):
			self.speed[i] = ((W * prev_speed) + (C1 * r1 * (self.p_best[i] - self.coord[i])) +
							 (C2 * r2 * (self.g_best[i] - self.coord[i])))
		
	def update_position(self):
		self.coord = [(self.coord[i] + self.speed[i]) for i in range(0, self.ndim)]
		for i in range(0, self.ndim):
			if self.coord[i] > self.xmax: self.coord[i] = self.xmax
			elif self.coord[i] < self.xmin: self.coord[i] = self.xmin

particle = Particle()
particle.calc_fitness()
print(particle.fitness, particle.coord, particle.speed)
particle.update_speed(W=0.5, C1=0.1, C2=0.1)
particle.update_position()
particle.calc_fitness()
print("new values:", particle.fitness, particle.coord, particle.speed)