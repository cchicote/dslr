import math
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import describe
import pandas as pd
import seaborn as sns
import numpy as np
from utils import *

def prepare_dataset(dataset):
    # The results data will have this format:
    # {'Class1': {'House1': [grades], 'House2': [grades]}}
    results = {}
    grade_min, grade_max = {}, {}
    for course in classes:
        if course not in results.keys():
            results[course] = {}
    list_size = int(dataset['Index'][len(dataset['Index']) - 1])
    for i in range(list_size + 1):
        for course in classes:
            try:
                house = dataset['Hogwarts House'][i]
                if house == '':
                    continue
                grade = describe.try_float(dataset[course][i])
                if course not in grade_min.keys() or grade < grade_min[course]:
                    grade_min[course] = grade
                if course not in grade_max.keys() or grade > grade_max[course]:
                    grade_max[course] = grade
                results[course][house].append(grade)
            except KeyError:
                results[course][house] = []
                results[course][house].append(grade)
    # Here we normalize our grades
    for course, houses in results.items():
        for house, grades in houses.items():
            for i in range(len(grades)):
                results[course][house][i] = normalize(results[course][house][i], grade_min[course], grade_max[course])
    return results

def plot_scatter_plotly(results):
    fig = go.Figure()
    for house in houses:
        grades = []
        for course_name in results.keys():
            grades.append(dict(label=course_name, values=results[course_name][house]))
        fig.add_trace(go.Splom(dimensions=grades, text=list(results.keys()), name=house, opacity=0.8, marker_color=houses_colors[house]))
    fig.show()

def plot_scatter_seaborn(filename):
    df = pd.read_csv(filename)
    graph = sns.pairplot(df, hue="Hogwarts House", vars=classes, plot_kws={'alpha':0.2}, diag_kind='hist', diag_kws={'alpha':0.6}, palette=houses_colors)
    plt.show()

def main():
    filename = 'datasets/dataset_train.csv'
    results = {}
    try:
        dataset = describe.retrieve_dataset(filename, fill_empty_nums=True)
    except FileNotFoundError:
        print("File not found, exiting program")
        exit()
    results = prepare_dataset(dataset)
    plot_scatter_plotly(results)
    plot_scatter_seaborn(filename)

if __name__ == "__main__":
    main()
