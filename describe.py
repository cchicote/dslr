<<<<<<< HEAD
#!env/bin/python3
import csv
=======
>>>>>>> 0efbfbe6ceb1cf2d752183e9533dd67e0802c3a9
import numpy as np
import math
from tabulate import tabulate
import parse

houses_colors = {'Gryffindor': '#7F0909', 'Slytherin': '#0D6217', 'Hufflepuff': '#EEE117', 'Ravenclaw': '#000A90'}

def warn_diff(feature, val_type, standard_val, local_val):
    print("DIFF FOR: [%s] [%s] [%f] [%f]" % (feature, val_type, standard_val, local_val))
    
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

def my_count(values):
    count = 0.0
    for value in values:
        if not np.isnan(value):
            count += 1
    return count

def my_sum(values):
    s = 0
    for value in values:
        if not np.isnan(value):
            s += value
    return s

def my_mean(values, count=None):
    if count is None:
        count = my_count(values)
    if count > 0:
        return (my_sum(values) / count)
    else:
        print("Error in my_mean: counted [%f] elements in values" % (count))
        return None
    

def my_std(values, mean, ddof=1, count=None):
    # We set count default value as None so that if feature has already been counted, we can just pass it as a parameter instead of calculating again in the 
    # function, but the function still keeps the ability to count the feature
    total = 0.0
    if count is None:
        count = my_count(values)
    if count > 0:
        for value in values:
            if not np.isnan(value):
                total += abs(value - mean)**2
        std = np.sqrt(total / (count - ddof))
        return std
    else:
        print("Error in my_std: counted [%f] elements in values" % (count))
        return None

def my_quantile(values, quantile, count=None):
    # Pure-Python implementation of percentile function: https://stackoverflow.com/a/2753343
    duplicate = values.copy()
    duplicate.sort_values(inplace=True)
    if count is None:
        count = my_count(values)
    if count > 0:
        k = (count -1) * quantile
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return (duplicate.iloc[int(k)])
        d0 = duplicate.iloc[int(f)] * (c-k)
        d1 = duplicate.iloc[int(c)] * (k-f)
        return d0+d1
    else:
        print("Error in my_quantile: counted [%f] elements in values" % (count))
        
def format_output(describe):
    # Returning a dict with the same structure as the pandas describe function
    out = {}
    out[""] = []
    for val_type in describe[next(iter(describe))]:
        out[""].append(val_type)
    for feature in describe.keys():
        out[feature] = []
        for val_type in out[""]:
            out[feature].append(describe[feature][val_type])
    return out

def my_describe(df, df_orig, print_describe=True):
    # "Delta Degrees of Freedom" - Not exactly sure of what it does with such dataframes
    ddof = 1

    # Values calculated with our functions go to describe dict
    describe = {}
    # Values calculated with system/numpy functions go to control_values dict
    # It will allow us to check if our functions return correct values
    control_values = df_orig.describe()
    
    for feature in df:
        describe[feature] = {}
        describe[feature]["count"] = my_count(df[feature])
        describe[feature]["mean"] = my_mean(df[feature], count=describe[feature]["count"])
        describe[feature]["std"] = my_std(df[feature], describe[feature]["mean"], ddof=ddof, count=describe[feature]["count"])
        describe[feature]["min"] = my_min(df[feature])
        describe[feature]["25%"] = my_quantile(df[feature], .25, count=describe[feature]["count"])
        describe[feature]["50%"] = my_quantile(df[feature], .5, count=describe[feature]["count"])
        describe[feature]["75%"] = my_quantile(df[feature], .75, count=describe[feature]["count"])
        describe[feature]["max"] = my_max(df[feature])

        # For each significative difference between results from our functions and results from system/numpy functions, we output a warning
        for value in control_values[feature].keys():
            if not np.isclose(describe[feature][value], control_values[feature][value]):
                warn_diff(feature, value, describe[feature][value], control_values[feature][value])

    if print_describe is True:
        print(tabulate(format_output(describe), headers="keys", tablefmt="fancy_grid", floatfmt=".6f"))
        print(tabulate(df_orig.describe(), headers="keys", tablefmt="fancy_grid", floatfmt=".6f"))

    return describe

def main():
    # Read CSV file with pandas
    df_orig = parse.read_file("datasets/dataset_train.csv")

    # Trim the dataframe to avoid nans and keep only the numeric values that will be used in calculations
    df = parse.trim_dataframe(df_orig.copy())

    # Describe
    desc = my_describe(df, df_orig)

if __name__ == "__main__":
    main()