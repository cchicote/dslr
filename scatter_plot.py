#!dslr_env/bin/python3
import plotly.graph_objects as go
import parse

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
	args = parse.get_args_ds()
	if args == -1:
		return
	df = parse.read_file(args.fname_dataset)

	# Plot the normalized data for each feature
	my_scatter_plot(parse.normalize_df(df.copy()))

if __name__ == "__main__":
	main()
