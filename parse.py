import pandas as pd
import describe
import math

numeric_values = ["float64", "int64"]

def normalize_df(df):
    for column in df.columns:
        if df[column].dtype not in numeric_values:
            continue
        df[column] = (df[column] - describe.my_min(df[column])) / (describe.my_max(df[column]) - describe.my_min(df[column]))
    return df

#def normalize_df(df):
#    return df.apply(lambda x: (x - describe.my_min(x)) / (describe.my_max(x) - describe.my_min(x)) if (describe.my_min(x) != describe.my_max(x)) else 0)

def read_file(filename):
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print("File not found, exiting program")
    except OSError:
        print("OSError raised reading the file, exiting program")
    except pd.errors.ParserError:
        print("Invalid file, exiting program")
    else:
        return df
    exit(1)
