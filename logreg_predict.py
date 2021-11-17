#!dslr_env/bin/python3

import sys
from logreg_train import Rocky
import constants as cst
import numpy as np
import parse

feat_list = ['Astronomy', 'Herbology', 'Ancient Runes', 'Defense Against the Dark Arts', 'Divination', 'Transfiguration']

def	predict(rocky):
	print("=============PREDICT=============")
	output = []
	for house in range(len(cst.houses)):
		res = rocky.sigmoid(np.dot(rocky.theta[:, house], rocky.x.T) + rocky.bias)
		output.append(res)

	output = np.array(output)
	max = np.amax(output, axis=0)
	ret = []
	for i in range(rocky.m):
		bruh = np.where(output[:,i] == max[i])
		ret.append(bruh[0][0])

	return ret

def	accuracy(rocky):
	output = predict(rocky)
	print("=============ACCURACY=============")
	accuracy = 0
	l = 0
	for col in range(len(cst.houses)):
		for row in range(rocky.m):
			if rocky.y[row, col] == 1 and output[row] == col:
				accuracy += 1
			l+= 1

	accuracy = accuracy * 100 / rocky.m
	print(accuracy)

def main():
	filename = parse.get_filename(sys.argv, len(sys.argv))
	df = parse.normalize_df(parse.read_file(filename))
	df1 = df.copy()[['Hogwarts House'] + feat_list]
	df1.dropna(inplace=True)
	rocky = Rocky(df1)
	rocky.load_thetas("weights.pkl")
	accuracy(rocky)

if __name__ == "__main__":
	main()
