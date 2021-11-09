import plotly.graph_objects as go
import parse
import describe

def my_histogram(df):
    fig = go.Figure()
    for feature in df:
        # Skip the Index column and the features that do not contain exclusively numeric values
        if feature == "Index" or df[feature].dtype not in parse.numeric_values:
            continue
        count = describe.my_count(df[feature])
        std = describe.my_std(df[feature], describe.my_mean(df[feature], count=count), ddof=1, count=count)
        fig.add_trace(go.Histogram(histfunc="avg", x=[feature], y=[std], name=feature, opacity=0.8))

    fig.update_layout(title="Standard deviation between the student's grades for each feature (less std means that the student's grades are homogeneous)", xaxis_title="Feature", yaxis_title="Standard deviation")
    fig.show()

def main():
    # Read CSV file with pandas
    df_orig = parse.read_file("datasets/dataset_train.csv")

    # Normalize the values of the dataframe
    df = parse.normalize_df(df_orig.copy())

    # Calculate the standard deviation for each feature and plot it
    my_histogram(df)

if __name__ == "__main__":
    main()
