from concurrent.futures import ProcessPoolExecutor
from Particle import Particle
from termcolor import colored
from datetime import datetime
from main import update_neighbors, generation_log
import multiprocessing
from tqdm import tqdm
import itertools
import pickle

def run(prmt):
    
    p = {"MAX_ITR": prmt[0],
        "M": prmt[1],
        "W": prmt[2],
        "C1": prmt[3],
        "C2": prmt[4],
        "XMIN": prmt[5],
        "XMAX": prmt[6]}

    particle_cloud = [Particle(xmin=p['XMIN'], xmax=p['XMAX']) for _ in range(0, p["M"])]
    log_fitness = []
    for _ in range(0, p["MAX_ITR"]):

        # Insere os vizinhos de cada particula
        update_neighbors(particle_cloud, p["M"])

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
            current_particle.update_speed(p["W"], p["C1"], p["C2"])

            # Atualiza a posição da Particula de acordo com a nova velocidade
            current_particle.update_position()
            
            particle_cloud[i] = current_particle
        
        log_fitness.append(generation_log(particle_cloud))
    
    return log_fitness, p

MAX_ITR = [50, 100, 150, 200, 250]
M = [100, 200, 300, 400, 500]
W = [0.1, 0.15, 0.2]
C1 = [0.1, 0.15, 0.2]
C2 = [0.1, 0.15, 0.2]
XMIN = [-10]
XMAX = [10]

all_list = [MAX_ITR, M, W, C1, C2, XMIN, XMAX]
parameters = list(itertools.product(*all_list)) 

executor = ProcessPoolExecutor()
num_args = len(parameters)
chunksize = int(num_args/multiprocessing.cpu_count())
results = [i for i in tqdm(executor.map(run, parameters),total=num_args)]

pickle.dump(results, open("Results/results_"+str(len(parameters))+"_.pickle", "wb"))