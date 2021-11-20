#!dslr_env/bin/python3
import numpy as np
from tabulate import tabulate
import parse
import describe as dc

def warn_diff(feature, val_type, standard_val, local_val):
    print("DIFF FOR: [%s] [%s] [%f] [%f]" % (feature, val_type, standard_val, local_val))

def test_describe(df, describe, print_describe=True):
    # Values calculated with system/numpy functions go to control_values dict
    # It will allow us to check if our functions return correct values
    feat_list = parse.get_features_list(df)
    control_values = df.describe().loc[:, feat_list[0]:]
    errors = 0
    
    for feature in df:
        # Skip the features that do not contain exclusively numeric values
        if feature not in feat_list:
            continue

        # For each significative difference between results from our functions and results from system/numpy functions, we output a warning
        for value in control_values[feature].keys():
            if not np.isclose(describe[feature][value], control_values[feature][value]):
                errors += 1
                warn_diff(feature, value, describe[feature][value], control_values[feature][value])

    if print_describe is True:
        print(tabulate(describe, headers="keys", tablefmt="fancy_grid", floatfmt=".6f"))
        print(tabulate(control_values, headers="keys", tablefmt="fancy_grid", floatfmt=".6f"))

    return errors

def main():
    args = parse.get_args_ds()
    if args == -1:
        return
    df = parse.read_file(args.fname_dataset)

    # Describe
    test_describe(df, dc.get_data(df))

if __name__ == "__main__":
    main()

