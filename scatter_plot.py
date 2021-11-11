#!dslr_env/bin/python3
import plotly.graph_objects as go
import parse
import constants as cst

def my_scatter_plot(df):
	fig = go.Figure()
	feat_list = parse.get_features_list(df)
	for feature in df:
		# Skip the Index column and the features that do not contain exclusively numeric values
		if feature not in feat_list:
			continue
		fig.add_trace(go.Scatter(y=df[feature], name=feature, opacity=0.8, mode='markers'))

	fig.update_layout(title="Normalized grades for each class", xaxis_title="Index", yaxis_title="Normalized grades")
	fig.show()

def main():
	# Read CSV file with pandas
	df_orig = parse.read_file("datasets/dataset_train.csv")

	# Normalize the values of the dataframe
	df = parse.normalize_df(df_orig.copy())

	# Plot the normalized data for each feature
	my_scatter_plot(df)

if __name__ == "__main__":
	main()
