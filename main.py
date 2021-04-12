from Particle import Particle
from tqdm import tqdm
import plot_charts as pc
import numpy as  np
import argparse

def update_neighbors(particle_cloud, M):
    for i in range(0, M):
        possible_neighbors = particle_cloud[:i] + particle_cloud[i+1:]
        particle_cloud[i].set_neighbors(possible_neighbors)

def generation_log(particle_cloud):
    particle_fitness = [p.fitness for p in particle_cloud]
    mean_fit = np.mean(particle_fitness)
    median_fit = np.median(particle_fitness)
    std_fit = np.std(particle_fitness)
    best_solution = min(particle_cloud, key=lambda x: x.calc_fitness(x.g_best))
    # return best_solution, mean_fit, median_fit, std_fit
    return best_solution.calc_fitness(best_solution.g_best), mean_fit, median_fit, std_fit

if __name__ == "__main__":

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

    # Cria a nuvem de particulas
    particle_cloud = [Particle(xmin=XMIN, xmax=XMAX) for _ in range(0, M)]
    log_fitness = []

    for itr in tqdm(range(0, MAX_ITR), position=0):

        # Insere os vizinhos de cada particula
        update_neighbors(particle_cloud, M)

        for i, current_particle in enumerate(particle_cloud):
            
            # Calcula o fitness da particula atual
            current_particle.update_fitness()
            
            # Atualiza p_best caso esse fitness seja melhor
            if current_particle.fitness <= current_particle.calc_fitness(current_particle.p_best):
                current_particle.p_best = current_particle.coord 

                # Se atualizar p_best, pode ser que atualize tambem o g_best
                if current_particle.fitness <= current_particle.calc_fitness(current_particle.g_best):
                    current_particle.g_best = current_particle.coord

            # Atualiza a velocidade da particula
            current_particle.update_speed(W, C1, C2)

            # Atualiza a posição da Particula de acordo com a nova velocidade
            current_particle.update_position()
            
            particle_cloud[i] = current_particle
        
        log_fitness.append(generation_log(particle_cloud))

    # Melhor solução encontrada!
    best_solution = min(particle_cloud, key=lambda x: x.calc_fitness(x.g_best))
    print("=> Best Solution: ", best_solution.calc_fitness(best_solution.g_best), best_solution.g_best)

    parameters = { "MAX_ITR": MAX_ITR,
                "M": M,
                "W": W,
                "C1": C1,
                "C2": C2,
                "XMIN": XMIN,
                "XMAX": XMAX}

    pc.plot_graphics(log_fitness, parameters)