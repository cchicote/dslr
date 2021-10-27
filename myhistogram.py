#!env/bin/python3
import sys
import math
import pandas as pd
import mydescribe as describe

classes = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 
	'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']

def	histogram():
	csv = describe.get_csv('datasets/dataset_train.csv')
	
	ax = csv.hist(by='Hogwarts House', column='Arithmancy')
	print(ax)
	# print(csv.describe().loc[:,'Arithmancy':])

if __name__ == "__main__":
	histogram()