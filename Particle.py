import random

class Particle:

	def __init__(self, ndim=4, xmin=-3, xmax=3):
		self.fitness = None
		self.ndim = ndim
		self.xmin = xmin
		self.xmax = xmax
		self.speed = []
		self.p_best = []
		self.g_best = []
		self.coord = self.__initial_coord()
		
	def __initial_coord(self):
		return [random.uniform(self.xmin, self.xmax) for _ in range(self.ndim)]

	def calc_fitness(self):
		self.fitness = self.__colville()

	def __colville(self):
		x1, x2, x3, x4 = self.coord
		return (100*(x1 - (x2**2))**2 + (1 - x1)**2 + 90*(x4 - x3)**2 + (1 - x3)**2 +
			    10.1*((x2 - 1)**2 + (x4 - 1)**2) + 19.8*(x2 - 1)*(x4 - 1))


particle = Particle()
particle.calc_fitness()
print(particle.fitness)