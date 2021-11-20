#!dslr_env/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import parse
import constants as cst

def get_classes(df):
	classes = []
	feat_list = parse.get_features_list(df)
	for feature in df:
		# Skip the Index column and the features that do not contain exclusively numeric values
		if feature not in feat_list:
			continue
		classes.append(feature)
	return classes

def my_pair_plot(df, classes):
	graph = sns.pairplot(pd.DataFrame(df), hue="Hogwarts House", vars=classes, plot_kws={'alpha': 0.2}, diag_kind='hist', diag_kws={'alpha':0.6}, palette=cst.houses_colors)
	plt.show()

def main():
	# Read CSV file with pandas
	args = parse.get_args_ds()
	if args == -1:
		return
	df = parse.read_file(args.fname_dataset)

	# Normalize a copy of the dataframe
	df_norm = parse.normalize_df(df.copy())

	# Pair plot the normalized grades for each class and each house
	my_pair_plot(df_norm, get_classes(df_norm))

if __name__ == "__main__":
	main()
