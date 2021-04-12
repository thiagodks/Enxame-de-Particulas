import matplotlib.pyplot as plt
from termcolor import colored

def plot_graphics(gen_log, args, name=""):

	gen_log = list(map(list, zip(*gen_log)))
	p_best, mean_fitness, median_fitness = gen_log[0], gen_log[1], gen_log[2]

	fig, (ax1, ax2) = plt.subplots(1,2)
	fig.set_size_inches(20, 7)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(top=0.80)
	
	itr = len(p_best)
	ax1.set_title("Fitness a cada Iteração")
	ax1.set_xlabel("Iterações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, itr)), p_best, 'g--', label='Melhor Fitness: %.4f' % p_best[-1])
	ax1.legend(ncol=1)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness")
	ax2.set_xlabel("Iterações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(0, itr)), p_best, 'g--', label='Melhor Fitness: %.4f' % (p_best[-1]))
	ax2.plot(list(range(0, itr)), mean_fitness, 'b--', label='Media: %.4f' % (mean_fitness[-1]))
	ax2.plot(list(range(0, itr)), median_fitness, 'y--', label='Mediana: %.4f' % (median_fitness[-1]))
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	print(colored("\033[1m"+"-> Gráfico salvo em: ", "green"), 'Graficos/'+name+"_"+str(args)+'_.pdf')
	fig.savefig('Graficos/'+name+"_"+str(args)+'_.pdf')
