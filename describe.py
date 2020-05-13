import csv
import math

def calculate_mean(data):
    total = 0.0
    for element in data:
        if element == '':
            element = 0.0
        total += float(element)
    return total / len(data)

dataset = {}
with open('datasets/dataset_train.csv', 'r') as file:
    reader = csv.reader(file)
    dataset = dict.fromkeys(next(reader), 0)
    for row in reader:
        for i in range (len(dataset.keys())):
            if (dataset[list(dataset.keys())[i]] == 0):
                dataset[list(dataset.keys())[i]] = []
            dataset[list(dataset.keys())[i]].append(row[i])

print('\t\t', end='')
for key in dataset.keys():
    #try:
    #    calculate_mean(dataset[key])
    #except ValueError as e:
    #    pass
    #else:
    print(key, end='\t\t')
print('')

''' count '''
print('Count', end='\t\t')
for key in dataset.keys():
    #try:
    #    calculate_mean(dataset[key])
    #except ValueError:
    #    # pass
    #else:
    print(len(dataset[key]), end='\t\t')
print('')

''' mean '''
print('Mean', end='\t\t')
for key in dataset.keys():
    try:
        mean = calculate_mean(dataset[key])
    except ValueError:
        #pass
        print(None, end='\t\t')
    else:
        print("%.2f" % (mean), end='\t\t')
print('')

''' std '''
print('Std', end='\t\t')
for key in dataset.keys():
    try:
        mean = calculate_mean(dataset[key])
        total = 0.0
        for element in dataset[key]:
            if element == '':
                element = 0.0
            total += abs(float(element) - mean)**2
        std = math.sqrt(total / len(dataset[key]))
    except ValueError:
        #pass
        print(None, end='\t\t')
    else:
        print("%.2f" % (std), end='\t\t')
print('')

''' min '''
print('Min', end='\t\t')
for key in dataset.keys():
    try:
        min_value = None
        for element in dataset[key]:
            if element == '':
                element = 0.0
            if (min_value is None) or (float(element) < min_value):
                min_value = float(element)
    except ValueError:
       # pass
        print(None, end='\t\t')
    else:
        print("%.2f" % (min_value), end='\t\t')
print('')

''' max '''
print('Max', end='\t\t')
for key in dataset.keys():
    try:
        max_value = None
        for element in dataset[key]:
            if element == '':
                element = 0.0
            if (max_value is None) or (float(element) > max_value):
                max_value = float(element)
    except ValueError:
        #pass
        print(None, end='\t\t')
    else:
        print("%.2f" % (max_value), end='\t\t')
print('')

