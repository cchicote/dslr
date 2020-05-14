import csv
import numpy as np
import math

def calculate_mean(data):
    total = 0.0
    for element in data:
        if element == '':
            element = 0.0
        total += float(element)
    return total / len(data)

def try_float(value):
    if (value == ''):
        return 0.0
    else:
        return float(value)

def calculate_std(dataset, mean):
    total = 0.0
    for element in dataset:
        total += abs(element - mean)**2
    std = math.sqrt(total / len(dataset))
    return std

def calculate_quantile(dataset, quantile):
    #me = dataset[int((len(dataset) * quantile/100))]
    #numpy = np.percentile(dataset, quantile, interpolation='higher')
    #numpy = np.quantile(dataset, quantile/100, interpolation='higher')
    #if me != numpy:
    #    print("ERROR")
    #    print(len(dataset))
    #    print("Percentile: %d" % (quantile))
    #    print("My result: [%f]" % (me))
    #    print("Numpy's result: [%f]" % (numpy))
    #    print("")
    return dataset[int(len(dataset) * quantile/100)]

def get_max_len(description):
    max_len = 0
    for key, values in description.items():
        if len(key) > max_len:
            max_len = len(key)
        for value in values:
            if len(str(value)) > max_len:
                max_len = len(str(value))
    return max_len

def trim_dataset(values):
    # list.remove() raises a ValueError exception when there is no searched element in the list
    return_values = values.copy()
    try:
        while True:
            return_values.remove('')
    except ValueError:
        return return_values

def print_description(description):
    max_len = get_max_len(description) + 2
    for key, values in description.items():
        printable = [key] + list(map(str, values))
        print("".join(word.ljust(max_len) for word in printable))

def describe_dataset(dataset):
    description = {}
    description['keys'] = []
    description['count'] = []
    description['mean'] = []
    description['std'] = []
    description['min'] = []
    description['25'] = []
    description['50'] = []
    description['75'] = []
    description['max'] = []

    for key in dataset.keys():
        #trimmed_data = trim_dataset(dataset[key])
        trimmed_data = dataset[key]
        description['keys'].append(key)
        description['count'].append(len(trimmed_data))
        try:
            float_data = list(map(try_float, trimmed_data))
            sorted_float_data = sorted(float_data)
            mean = calculate_mean(float_data)
            description['mean'].append(mean)
            description['std'].append(calculate_std(float_data, mean))
            description['min'].append(sorted_float_data[0])
            description['25'].append(calculate_quantile(sorted_float_data, 25))
            description['50'].append(calculate_quantile(sorted_float_data, 50))
            description['75'].append(calculate_quantile(sorted_float_data, 75))
            description['max'].append(sorted_float_data[len(sorted_float_data) - 1])
        except ValueError:
            # A ValueError exception means that the feature is not made of numbers so we can't calculate all of these values
            description['mean'].append(None)
            description['std'].append(None)
            description['min'].append(None)
            description['25'].append(None)
            description['50'].append(None)
            description['75'].append(None)
            description['max'].append(None)
    return description

def main():
    dataset = {}
    with open('datasets/dataset_train.csv', 'r') as file:
        reader = csv.reader(file)
        dataset = dict.fromkeys(next(reader), 0)
        for row in reader:
            for i in range (len(dataset.keys())):
                if (dataset[list(dataset.keys())[i]] == 0):
                    dataset[list(dataset.keys())[i]] = []
                dataset[list(dataset.keys())[i]].append(row[i])
    description = describe_dataset(dataset)
    print_description(description)
    exit()

if __name__ == '__main__':
    main()

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


''' quartile_25 '''
print('25%', end='\t\t')
for key in dataset.keys():
    try:
        data = sorted(list(map(float, dataset[key])))
        quartile_25 = calculate_quantile(data, 25) 
        numpy_25 = np.quantile(data, 0.25)
    except ValueError:
        print(None, end='\t\t')
    else:
        print("%.2f" % (quartile_25), end='\t\t')
        print("NUMPY: %.2f" % (numpy_25), end='\t\t')
print('')

''' quartile_50 '''
print('50%', end='\t\t')
for key in dataset.keys():
    try:
        data = sorted(list(map(float, dataset[key])))
        quartile_50 = calculate_quantile(data, 50) 
    except ValueError:
        print(None, end='\t\t')
    else:
        print("%.2f" % (quartile_50), end='\t\t')
print('')

''' quartile 75 '''
print('75%', end='\t\t')
for key in dataset.keys():
    try:
        data = sorted(list(map(float, dataset[key])))
        quartile_75 = calculate_quantile(data, 75) 
    except ValueError:
        print(None, end='\t\t')
    else:
        print("%.2f" % (quartile_75), end='\t\t')
print('')

