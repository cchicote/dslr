#!env/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import parse
import constants as cst

def get_classes(df):
	classes = []
	for feature in df:
		# Skip the Index column and the features that do not contain exclusively numeric values
		if feature == "Index" or df[feature].dtype not in parse.numeric_values:
			continue
		classes.append(feature)
	return classes

def my_pair_plot(df, classes):
	graph = sns.pairplot(pd.DataFrame(df), hue="Hogwarts House", vars=classes, plot_kws={'alpha': 0.2}, diag_kind='hist', diag_kws={'alpha':0.6}, palette=cst.houses_colors)
	plt.show()

def main():
	# Read CSV file with pandas
	df_orig = parse.read_file("datasets/dataset_train.csv")

	# Normalize a copy of the dataframe
	df = parse.normalize_df(df_orig.copy())

	# Pair plot the normalized grades for each class and each house
	my_pair_plot(df, get_classes(df))

if __name__ == "__main__":
	main()
