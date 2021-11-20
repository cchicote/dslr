#!dslr_env/bin/python3
import matplotlib.pyplot as plt
import describe as describe
import constants as cst
import parse

def	get_feature_per_house(df, house, feature):
	feature_per_house = df[df["Hogwarts House"] == house][feature]
	return feature_per_house

def	plot_hist(df):
	i=0
	j=0
	fig, axs = plt.subplots(4, 4)
	feat_list = parse.get_features_list(df)
	for feature in df:
		if feature not in feat_list:
			continue
		for house in cst.houses:
			axs[i, j].hist(get_feature_per_house(df, house, feature), bins=25, alpha=0.5, color = cst.houses_colors[house])
			axs[i, j].set_title(feature)
		j += 1
		if j == 4:
			i += 1
			j = 0
	plt.tight_layout()
	plt.show()

def	my_histogram(df):
	std = []
	feat_name = []
	n_feat = 0
	feat_list = parse.get_features_list(df)
	for feature in df:
		if feature not in feat_list:
			continue
		count = describe.get_count(df[feature])
		std.append(describe.get_std(count, describe.get_mean(count, df[feature]), df[feature]))
		feat_name.append(feature)
		n_feat += 1

	plt.bar(range(n_feat), std, color=cst.colors)
	plt.xticks(range(n_feat), feat_name, rotation=-45, fontsize=6, ha="left")
	plt.title("Standard deviation between the student's grades for each feature \n(less std means that the student's grades are homogeneous)")
	plt.show()

def	histogram():
	args = parse.get_args_ds()
	if args == -1:
		return
	df = parse.read_file(args.fname_dataset)
	plot_hist(parse.normalize_df(df))
	my_histogram(parse.normalize_df(df))

if __name__ == "__main__":
	histogram()
