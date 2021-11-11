#!dslr_env/bin/python3
import sys
import math
import pandas as pd
from tabulate import tabulate
import parse
import constants as cst

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

def	get_var(std):
	return std ** 2

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

def	get_data(df):
	feat_list = parse.get_features_list(df)
	description = pd.DataFrame(columns=feat_list)

	for feature in df:
		if feature not in feat_list:
			continue

		values = df[feature]

		count = get_count(values)
		mean = get_mean(count, values)
		description.loc['count', feature] = count
		description.loc['mean', feature] = mean
		std = get_std(count, mean, values)
		description.loc['std', feature] = std
		description.loc['var', feature] = get_var(std)

		data = values.sort_values(ignore_index=True)

		description.loc['min', feature] = data.loc[0]
		description.loc['25%', feature] = get_percent(data, 0.25, count)
		description.loc['50%', feature] = get_percent(data, 0.50, count)
		description.loc['75%', feature] = get_percent(data, 0.75, count)
		description.loc['max', feature] = data.loc[count - 1]

	return description

def	describe():
	filename = parse.get_filename(sys.argv, len(sys.argv))
	df = parse.read_file(filename)
	
	description = get_data(df)

	print(tabulate(description, cst.classesHeaders, tablefmt="fancy_grid", numalign=("right")))

if __name__ == "__main__":
	describe()
