#!env/bin/python3
import sys
import math
import pandas as pd
from tabulate import tabulate
import constants as cst

def	parsing(av, ac):
	if ac != 2:
		print("usage: ./describe.py [dataset]")
		exit()
	return av[1]

def	get_csv(path):
	try:
		csv = pd.read_csv(path, sep=",")
	except:
		print ("data.csv file missing")
		sys.exit()
	return csv

def	get_count(values):
	count = 0.0
	for elem in values:
		if math.isnan(elem):
			continue
		count += 1
	return count

def	get_mean(count, values):
	mean = 0.0
	for elem in values:
		if math.isnan(elem):
			continue
		mean += elem
	mean /= count
	return mean

def	get_std(count, mean, values):
	summ = 0.0
	for elem in values:
		if math.isnan(elem):
			continue
		summ += abs(elem - mean) ** 2
	std = math.sqrt(summ / (count - 1))
	return std

def	get_var(count, mean, values):
	var = 0.0
	for elem in values:
		if math.isnan(elem):
			continue
		var += (elem - mean) ** 2
	var = math.sqrt(var / count)
	return var

def	get_percent(data, percent, count):
	if count > 0:
		k = (count -1) * percent
		f = math.floor(k)
		c = math.ceil(k)
		if f == c:
			return (data.iloc[int(k)])
		d0 = data.iloc[int(f)] * (c-k)
		d1 = data.iloc[int(c)] * (k-f)
		return d0+d1
	else:
		print("Error in my_quantile: counted [%f] elements in values" % (count))

def	get_data(description, csv):
	for classe in csv:
		if classe not in cst.classes:
			continue

		values = csv.loc[:, classe]

		count = get_count(values)
		mean = get_mean(count, values)
		description.loc['Count', classe] = count
		description.loc['Mean', classe] = mean
		std = get_std(count, mean, values)
		print("count=",count, ", mean=", mean, "std=", std)
		description.loc['Std', classe] = std
		description.loc['Var', classe] = get_var(count, mean, values)

		data = values.sort_values(ignore_index=True)

		description.loc['Min', classe] = data.loc[0]
		description.loc['25%', classe] = get_percent(data, 0.25, count)
		description.loc['50%', classe] = get_percent(data, 0.50, count)
		description.loc['75%', classe] = get_percent(data, 0.75, count)
		description.loc['Max', classe] = data.loc[count - 1]

def	describe():
	path = parsing(sys.argv, len(sys.argv))
	csv = get_csv(path)
	description = pd.DataFrame(columns=cst.classes)

	get_data(description, csv)

	print("My describe:")
	print(tabulate(description, cst.classesHeaders, tablefmt="fancy_grid", numalign=("right")))
	print("\nDescribe from pd.describe():")
	print(tabulate(csv.describe().loc[:,'Arithmancy':], cst.classesHeaders, tablefmt="fancy_grid", numalign=("right")))

if __name__ == "__main__":
	describe()