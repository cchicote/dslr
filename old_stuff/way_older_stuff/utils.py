classes = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 
	'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
houses_colors = {'Gryffindor': '#7F0909', 'Slytherin': '#0D6217', 'Hufflepuff': '#EEE117', 'Ravenclaw': '#000A90'}

def get_min(values):
    return sorted(values)[0]

def get_max(values):
    return sorted(values)[len(values) - 1]

def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

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


