#!env/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import describe as describe
import constants as cst

def	preprocess(csv):
	data = csv.copy()
	for classe in cst.classes:
		count = describe.get_count(csv.loc[:, classe])
		mean = describe.get_mean(count, csv.loc[:, classe])
		std = describe.get_std(count, mean, csv.loc[:, classe])
		data[classe] = (data[classe] - mean) / std
	return data[cst.classes]

def	get_grades(csv, data, house, topic):
	df = data[csv["Hogwarts House"] == house][topic]
	df.dropna(inplace=True)
	return df

def	plot_hist(csv, data):
	i=0
	j=0
	fig, axs = plt.subplots(4, 4)
	for col in data.columns:
		axs[i, j].hist(get_grades(csv, data, "Gryffindor", col), bins=25, alpha=0.5, label = 'Gry', color = '#7F0909')
		axs[i, j].hist(get_grades(csv, data, "Ravenclaw", col), bins=25, alpha=0.5, label = 'Rav', color = '#000A90')
		axs[i, j].hist(get_grades(csv, data, "Slytherin", col), bins=25, alpha=0.5, label = 'Sly', color = '#0D6217')
		axs[i, j].hist(get_grades(csv, data, "Hufflepuff", col), bins=25, alpha=0.5, label = 'Huf', color = '#EEE117')
		axs[i, j].set_title(col)
		j += 1
		if j == 4:
			i += 1
			j = 0
	plt.tight_layout()
	plt.show()

def	my_min(values):
	m = values[0]
	for value in values:
		if m < value:
			m = value
	return m

def	my_max(values):
	m = values[0]
	for value in values:
		if m > value:
			m = value
	return m

def	normalize(csv):
	nrmlz_csv = pd.DataFrame(columns=cst.classes)
	for classe in csv:
		if classe not in cst.classes:
			continue
		min_value = my_min(csv[classe])
		max_value = my_max(csv[classe])
		for idx, value in enumerate(csv.loc[:,classe]):
			nrmlz_csv.loc[idx, classe] = float((value - min_value) / (max_value - min_value))
	return nrmlz_csv

def	my_histogram(csv):
	std = []
	nrmlz_csv = normalize(csv)
	for classe in cst.classes:
		values = nrmlz_csv.loc[:, classe]

		count = describe.get_count(values)
		mean = describe.get_mean(count, values)
		std.append(describe.get_std(count, mean, values))

	plt.bar(range(13), std, color=cst.colors)
	plt.xticks(range(13), cst.classesHeaders, rotation=-45, fontsize=6, ha="left")
	plt.title("Standard deviation between the student's grades for each feature \n(less std means that the student's grades are homogeneous)")
	plt.show()

def	histogramme():
	csv = pd.read_csv(sys.argv[1], sep=",")
	data = preprocess(csv)
	plot_hist(csv, data)
	my_histogram(csv)

if __name__ == "__main__":
	histogramme()