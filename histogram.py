import math
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import describe

classes = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
houses_colors = {'Gryffindor': '#7F0909', 'Slytherin': '#0D6217', 'Hufflepuff': '#EEE117', 'Ravenclaw': '#000A90'}

def get_min(values):
    return sorted(values)[0]

def get_max(values):
    return sorted(values)[len(values) - 1]

def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

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
                grade = describe.try_float(dataset[course][i])
                results[course][house].append(grade)
                if course not in grade_min.keys() or grade < grade_min[course]:
                    grade_min[course] = grade
                if course not in grade_max.keys() or grade > grade_max[course]:
                    grade_max[course] = grade
            except KeyError:
                    results[course][house] = []
                    results[course][house].append(grade)
    # Here we normalize our grades
    for course, houses in results.items():
        for house, grades in houses.items():
            for i in range(len(grades)):
                results[course][house][i] = normalize(results[course][house][i], grade_min[course], grade_max[course])
    return results

def calculate_variance(grades):
    squared_grades_total, squared_grades_mean = 0, 0
    grades_total, grades_mean = 0, 0
    grades_min, grades_max = get_min(grades), get_max(grades)
    for grade in grades:
        squared_grades_total += grade **2
        grades_total += grade
    squared_grades_mean = squared_grades_total / len(grades)
    grades_mean = grades_total / len(grades)
    return squared_grades_mean - (grades_mean ** 2)

def variance_per_course_per_house(dataset):
    # The results data will have this format:
    # {'Class1': {'House1': variance, 'House2': variance}}
    results = {}
    for course in classes:
        if course not in results.keys():
            results[course] = {}
    for course in dataset.keys():
        for house in dataset[course].keys():
            results[course][house] = calculate_variance(dataset[course][house])
    return results

def plot_histogram(results_variance):
    fig = go.Figure()
    variance_per_house = {}
    grades_per_house = {}
    for course in results_variance.keys():
        for house in results_variance[course]:
            if house not in variance_per_house.keys():
                variance_per_house[house] = []
            variance_per_house[house].append(results_variance[course][house])
    for house in variance_per_house.keys():
        fig.add_trace(go.Histogram(histfunc="avg", x=list(results_variance.keys()), y=variance_per_house[house], name=house, marker_color=houses_colors[house], opacity=0.8))
    fig.update_layout(title="Variances between the student's grades for each house and for each class (less variance means that the student's grades are homogeneous, more variance means that the student's grades are heterogeneous)", xaxis_title="Class", yaxis_title="Variance")
    fig.show()

def main():
    results = {}
    try:
        dataset = describe.retrieve_dataset('datasets/dataset_train.csv')
    except FileNotFoundError:
        print("File not found, exiting program")
        exit()
    results = prepare_dataset(dataset)
    results_variance = variance_per_course_per_house(results)
    plot_histogram(results_variance)

if __name__ == "__main__":
    main()
