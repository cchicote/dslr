import plotly.graph_objects as go
import parse
import describe

def my_scatter_plot(df):
    fig = go.Figure()
    for feature in df:
        if feature == "Index":
            continue
        fig.add_trace(go.Scatter(y=df[feature], name=feature, opacity=0.8, mode='markers'))

    fig.update_layout(title="Normalized grades for each class", xaxis_title="Index", yaxis_title="Normalized grades")
    fig.show()

def main():
    # Read CSV file with pandas
    df_orig = parse.read_file("datasets/dataset_train.csv")

    # Trim the dataframe to avoid nans and keep only the numeric values that will be used in calculations
    df = parse.trim_dataframe(df_orig.copy())

    # Plot the normalized data for each feature
    my_scatter_plot(parse.normalize_df(df))

if __name__ == "__main__":
    main()
