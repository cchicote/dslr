import pandas as pd
import numpy as np
import describe
import math
import constants as cst

def get_filename(av, ac):
	if ac != 2:
		print("usage: ./describe.py [dataset]")
		exit()
	return av[1]

def my_min(values):
    m = values[0]
    for value in values:
        if not np.isnan(value):
            if value < m:
                m = value
    return m

def my_max(values):
    m = values[0]
    for value in values:
        if not np.isnan(value):
            if value > m:
                m = value
    return m

def get_features_list(df):
	feat_list = []
	for feature in df:
		if feature == "Index" or df[feature].dtype not in cst.numeric_values:
			continue
		feat_list.append(feature)
	return feat_list

def normalize_df(df):
    for column in df.columns:
        if df[column].dtype not in cst.numeric_values:
            continue
        df[column] = (df[column] - my_min(df[column])) / (my_max(df[column]) - my_min(df[column]))
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
