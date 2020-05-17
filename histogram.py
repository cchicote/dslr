import math
import plotly.graph_objects as go
import describe

classes = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']

'''
def prepare_dataset(dataset):
    # The results data will have this format:
    # {'House': {'Class1': [grades], 'Class2': [grades]}}
    results = {}
    results['Gryffindor'] = {}
    results['Slytherin'] = {}
    results['Hufflepuff'] = {}
    results['Ravenclaw'] = {}
    list_size = int(dataset['Index'][len(dataset['Index']) - 1])
    for i in range(list_size + 1):
        house = ''
        for key in dataset.keys():
            if key == 'Hogwarts House':
                house = dataset[key][i]
            if key in classes:
                try:
                    grade = describe.try_float(dataset[key][i])
                    results[house][key].append(grade)
                except KeyError:
                    results[house][key] = []
                    results[house][key].append(grade)
'''

def prepare_dataset(dataset):
    # The results data will have this format:
    # {'Class1': {'House1': [grades], 'House2': [grades]}}
    results = {}
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
            except KeyError:
                    results[course][house] = []
                    results[course][house].append(grade)
    return results

def get_min(values):
    return sorted(values)[0]

def get_max(values):
    return sorted(values)[len(values) - 1]

def calculate_variance(grades):
    squared_grades_total, squared_grades_mean = 0, 0
    grades_total, grades_mean = 0, 0
    grades_min, grades_max = get_min(grades), get_max(grades)
    for grade in grades:
        normalized_grade = normalize(grade, grades_min, grades_max)
        squared_grades_total += normalized_grade **2
        grades_total += normalized_grade
    squared_grades_mean = squared_grades_total / len(grades)
    grades_mean = grades_total / len(grades)
    return squared_grades_mean - (grades_mean ** 2)

def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

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

    results_bis = {}
    for course in classes:
        if course not in results.keys():
            results[course] = {}
    variances_all = []
    for course in results.keys():
        variances = []
        for house in results[course].keys():
            variances.append(results[course][house])
        results_bis[course] = calculate_variance(variances)
        variances_all.append(results_bis[course])
    
    sorted_results_bis = {}
    for key in sorted(results_bis, key=results_bis.__getitem__):
        sorted_results_bis[key] = results_bis[key]

    print("Variance between students grades, per house per course")
    for key, value in results.items():
        print(key, value)

    print('\n')
    print("Variance between variance houses, per course")
    for key, value in results_bis.items():
        print(key, value)


#    fig = go.Figure(data=[go.Histogram(y=variances_all)])
 #   fig.show()


def main():
    result = {}
    try:
        dataset = describe.retrieve_dataset('datasets/dataset_train.csv')
    except FileNotFoundError:
        print("File not found, exiting program")
        exit()
    result = prepare_dataset(dataset)
    variance_per_course_per_house(result)

if __name__ == "__main__":
    main()
