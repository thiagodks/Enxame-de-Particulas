import matplotlib.pyplot as plt
from termcolor import colored
import pickle
import pandas as pd
from datetime import datetime
import argparse

def get_fitness(fitness):
	x1 = str(fitness)
	if x1.find("e") == -1: 
		return ("%.6f" % fitness)
	x2 = x1[:6]
	x2 += x1[x1.find("e"):]
	return x2

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
	ax1.plot(list(range(0, itr)), p_best, 'g--', label='Melhor Fitness: ' + get_fitness(p_best[-1]))
	ax1.legend(ncol=1)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness")
	ax2.set_xlabel("Iterações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(0, itr)), p_best, 'g--', label='Melhor Fitness: ' + get_fitness(p_best[-1]))
	ax2.plot(list(range(0, itr)), mean_fitness, 'b--', label='Media: ' + get_fitness(mean_fitness[-1]))
	ax2.plot(list(range(0, itr)), median_fitness, 'y--', label='Mediana: ' + get_fitness(median_fitness[-1]))
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	print(colored("\033[1m"+"-> Gráfico salvo em: ", "green"), 'Graficos/'+name+"_"+str(args)+'_.pdf')
	fig.savefig('Graficos/'+name+"_"+str(args)+'_.pdf')

def plot_table(results):

	table = {"$\\bf{ITR}$": [],
			"$\\bf{M}$": [],
			"$\\bf{W}$": [],
			"$\\bf{C1}$": [],
			"$\\bf{C2}$": [],
			"$\\bf{XMIN}$": [],
			"$\\bf{XMAX}$": [],
			"$\\bf{FIT}$": [],
			"$\\bf{MD}$": [],
			"$\\bf{ME}$": [],
			"$\\bf{STD}$": []}

	for i in results:
		cs = min(i[0], key=lambda x: x[0])
		table["$\\bf{ITR}$"].append(i[1]["MAX_ITR"])
		table["$\\bf{M}$"].append(i[1]["M"])
		table["$\\bf{W}$"].append(i[1]["W"])
		table["$\\bf{C1}$"].append(i[1]["C1"])
		table["$\\bf{C2}$"].append(i[1]["C2"])
		table["$\\bf{XMIN}$"].append(i[1]["XMIN"])
		table["$\\bf{XMAX}$"].append(i[1]["XMAX"])
		table["$\\bf{FIT}$"].append(get_fitness(cs[0]))
		table["$\\bf{ME}$"].append(get_fitness(cs[1]))
		table["$\\bf{MD}$"].append(get_fitness(cs[2]))
		table["$\\bf{STD}$"].append(get_fitness(cs[3]))

	df = pd.DataFrame(data=table)

	fig, ax = plt.subplots()

	fig.patch.set_visible(False)
	plt.axis("off")
	plt.grid("off")
	# fig.set_size_inches(4, 2)
	ax.set_title("Top-20 Execuções", y=0.99, fontdict={"fontsize": 6}, weight='bold')

	ncol = len(table.keys())
	colors = [["#ccccb3"] * ncol, ["#e0e0d1"] * ncol] * int(len(results)/2)
	the_table = ax.table(cellText=df.values,colLabels=df.columns, cellColours=colors, cellLoc="center", loc="center", colColours =["#78786d"] * ncol)
	the_table.auto_set_font_size(False)
	the_table.set_fontsize(6)

	fig.tight_layout()
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	fig.savefig("Tabelas/results_table_"+str(current_time)+".pdf", dpi=500, bbox_inches='tight')
	print(colored("\033[1m"+"\n-> Tabela salva em: " + "Tabelas/results_table_"+str(current_time)+".pdf", "green"))
	print("\nTabela: \n", df)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', required=True, type=str, help='Arquivo com os resultados fatoriais')
	args = vars(parser.parse_args())
	results = pickle.load(open(args['f'], 'rb'))
	results.sort(key=lambda x: min(x[0], key=lambda x: x[0]))
	plot_table(results[:20])
	plot_graphics(results[0][0], results[0][1], "best")
	plot_graphics(results[-1][0], results[-1][1], "worst")