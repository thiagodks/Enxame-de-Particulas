from Particle import Particle
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-itr', required=False, default=100, type=int, help='Número de Iterações')
parser.add_argument('-m', required=False, default=100, type=int, help='Número de Particulas')
parser.add_argument('-w', required=False, default=0.05, type=float, help='Ponderamento da velocidade')
parser.add_argument('-c1', required=False, default=0.01, type=float, help='Ponderamento p_best')
parser.add_argument('-c2', required=False, default=0.01, type=float, help='Ponderamento g_best')
parser.add_argument('-x1', required=False, default=-5, type=int, help='Valor de xmin')
parser.add_argument('-x2', required=False, default=5, type=int, help='Valor de xmax')
args = vars(parser.parse_args())

MAX_ITR = int(args['itr'])
M = int(args['m'])
W = float(args['w'])
C1 = float(args['c1'])
C2 = float(args['c2'])
XMIN = int(args['x1'])
XMAX = int(args['x2'])

def update_neighbors():
    for i in range(0, M):
        possible_neighbors = particle_cloud[:i] + particle_cloud[i+1:]
        particle_cloud[i].set_neighbors(possible_neighbors)

particle_cloud = [Particle(xmin=XMIN, xmax=XMAX) for _ in range(0, M)]

for itr in tqdm(range(0, MAX_ITR), position=0):

    update_neighbors()

    for i, current_particle in enumerate(particle_cloud):
        
        current_particle.update_fitness()
        
        if current_particle.fitness < current_particle.calc_fitness(current_particle.p_best):
            current_particle.p_best = current_particle.coord 

            if current_particle.fitness < current_particle.calc_fitness(current_particle.g_best):
                current_particle.g_best = current_particle.coord

        current_particle.update_speed(W, C1, C2)
        current_particle.update_position()
        
        particle_cloud[i] = current_particle

best_solution = min(particle_cloud, key=lambda x: x.calc_fitness(x.g_best))
print("GLOBAL FINAL: ", best_solution.fitness, best_solution.coord)