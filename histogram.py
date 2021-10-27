import plotly.graph_objects as go
import parse
import describe

def my_histogram(df):
    fig = go.Figure()
    for feature in df:
        count = describe.my_count(df[feature])
        std = describe.my_std(df[feature], describe.my_mean(df[feature], count=count), ddof=1, count=count)
        fig.add_trace(go.Histogram(histfunc="avg", x=[feature], y=[std], name=feature, opacity=0.8))

    fig.update_layout(title="Standard deviation between the student's grades for each feature (less std means that the student's grades are homogeneous)", xaxis_title="Feature", yaxis_title="Standard deviation")
    fig.show()

def main():
    # Read CSV file with pandas
    df_orig = parse.read_file("datasets/dataset_train.csv")

    # Trim the dataframe to avoid nans and keep only the numeric values that will be used in calculations
    df = parse.trim_dataframe(df_orig.copy())

    # Calculate the standard deviation for each feature and plot it
    my_histogram(parse.normalize_df(df))

if __name__ == "__main__":
    main()