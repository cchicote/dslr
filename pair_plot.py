#!env/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils import *

def parse(filename):
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
    exit()

def plot(dataframe):
    graph = sns.pairplot(dataframe, hue="Hogwarts House", vars=classes, plot_kws={'alpha':0.2}, diag_kind='hist', diag_kws={'alpha':0.6}, palette=houses_colors)
    plt.show()

def main():
    filename = 'datasets/dataset_train.csv'
    dataframe = parse(filename)
    plot(dataframe)

if __name__ == "__main__":
    main()
