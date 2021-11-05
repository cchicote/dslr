#!env/bin/python3
import sys
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mydescribe as describe

classes = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 
	'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
houses_colors = {'Gryffindor': '#7F0909', 'Slytherin': '#0D6217', 'Hufflepuff': '#EEE117', 'Ravenclaw': '#000A90'}

def preprocess(dataset):
	for classe in classes:
		dataset[classe] = (dataset[classe] - dataset[classe].mean()) / dataset[classe].std()
	return dataset[classes]

def get_grades(dataset, prep_dataset, house, topic):
	df = prep_dataset[dataset["Hogwarts House"] == house][topic]
	df.dropna(inplace=True)
	return df

def plot_hist(dataset, prep_dataset):
	i=0
	j=0
	fig, axs = plt.subplots(4, 4)
	for col in prep_dataset.columns:
		axs[i, j].hist(get_grades(dataset, prep_dataset, "Gryffindor", col), bins=25, alpha=0.5, label = 'Gry', color = '#7F0909')
		axs[i, j].hist(get_grades(dataset, prep_dataset, "Ravenclaw", col), bins=25, alpha=0.5, label = 'Rav', color = '#000A90')
		axs[i, j].hist(get_grades(dataset, prep_dataset, "Slytherin", col), bins=25, alpha=0.5, label = 'Sly', color = '#0D6217')
		axs[i, j].hist(get_grades(dataset, prep_dataset, "Hufflepuff", col), bins=25, alpha=0.5, label = 'Huf', color = '#EEE117')
		axs[i, j].set_title(col)
		j += 1
		if j == 4:
			i += 1
			j = 0
	plt.tight_layout()
	plt.show()

def my_histogram(df):
	std = []
	for classe in classes:
		count = describe.get_count(df.loc[:,classe])
		std.append(describe.get_std(count, describe.get_mean(count, df.loc[:,classe]), df.loc[:,classe]))
	"""
		le std marche pas je vais m en occuper
		mais pour l histogramme je te laisse gerer jy arrive pas j ai envie de casser mon ordi
	"""
	

def	histogramme():
	dataset = pd.read_csv(sys.argv[1], index_col = "Index")
	prep_dataset = preprocess(dataset)
	plot_hist(dataset, prep_dataset)
	my_histogram(dataset)

if __name__ == "__main__":
	histogramme()