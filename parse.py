import pandas as pd
import numpy as np
import describe
import math
import constants as cst
import argparse
from pathlib import Path

def get_filename(av, ac):
	if ac != 2:
		print("usage: ./describe.py [dataset]")
		exit()
	return av[1]

def check_path(args, parser):
    if Path(args.fname_dataset).suffix != '.csv':
        parser.print_help()
        return -1
    if Path(args.fname_weights).suffix != '.pkl':
        parser.print_help()
        return -1
    return args

def get_args_train():
    parser = argparse.ArgumentParser(description="Wonderful DSLR trainer.")
    parser.add_argument('-f', type=str, action="store", dest='fname_dataset', required=True, help='Format: <filename.csv>. Path to the dataset file')
    parser.add_argument('-w', type=str, action="store", dest='fname_weights', required=True, help='Format: <filename.pkl>. Path to the output file containing the weights from the training')
    parser.add_argument('-a', action="store_true", dest='accuracy', default=False, help='calculates accuracy (default: False)')
    args = parser.parse_args()
    return check_path(args, parser)

def get_args_predict():
    parser = argparse.ArgumentParser(description="Wonderful DSLR predictor.")
    parser.add_argument('-f', type=str, action="store", dest='fname_dataset', required=True, help='Format: <filename.csv>. Path to the dataset file')
    parser.add_argument('-w', type=str, action="store", dest='fname_weights', required=True, help='Format: <filename.pkl>. Path to the input file containing the weights from previous training')
    parser.add_argument('-a', action="store_true", dest='accuracy', default=False, help='calculates accuracy (default: False)')
    args = parser.parse_args()
    return check_path(args, parser)

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
