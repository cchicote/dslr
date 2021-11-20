#!dslr_env/bin/python3
import parse
import numpy as np
import pickle as pkl
import constants as cst

class Rocky():
	def __init__(self, df, learningRate = 0.9, it_max = 1000, tp = 100):
		self.df = df
		self.X = df.copy()[cst.feat_list].to_numpy()				# shape = student * features
		self.m, self.n = self.X.shape							# len student, len features
		self.y = self.get_binary_house()						# shape = student * houses
		self.theta = np.zeros(shape=(self.n, len(cst.houses)))	# shape = features * houses
		self.mt = int(tp * self.m / 100)
		self.mtest = self.m - self.mt
		self.x_train = self.X.copy()[:self.mt]
		self.x_test = self.X.copy()[self.mt:]
		self.y_train = self.y.copy()[:self.mt]
		self.y_test = self.y.copy()[self.mt:]
		self.cost = self.n
		self.it = 0
		self.it_max = it_max
		self.lr = learningRate

	def get_binary_house(self):
		y = np.zeros([self.m, len(cst.houses)])
		house = self.df.copy()["Hogwarts House"].to_numpy()
		for i in range(self.m):
			y[i, cst.houses.index(house[i])] = 1
		return y

	def	get_cost(self):
		pred = sigmoid(np.dot(self.x_train, self.theta))
		self.cost = -(1 / self.mt) * np.sum(self.y_train * np.log(pred) + (1 - self.y_train) * np.log(1 - pred))

	def update_theta(self, pred, house, feat):		
		dt = (1 / self.mt) * np.sum((pred - self.y_train[:,house]) * self.x_train[:,feat])
		self.theta[feat, house] -= self.lr * dt

	def gradient(self):
		for i in range(self.it_max):
			self.it = i
			self.get_cost()
			for house in range(len(cst.houses)):
				pred = sigmoid(np.dot(self.x_train, self.theta[:, house].T))
				for feat in range(self.n):
					self.update_theta(pred, house, feat)

def sigmoid(z):
	return 1.0 / (1 + np.exp(-z))

def	predict(theta, x, m):
	output = []
	for house in range(len(cst.houses)):
		res = sigmoid(np.dot(theta[:, house], x.T))
		output.append(res)

	output = np.array(output)
	max = np.amax(output, axis=0)
	ret = []
	for i in range(m):
		tmp = np.where(output[:,i] == max[i])
		ret.append(tmp[0][0])

	return ret

def	accuracy(rocky):
	output = predict(rocky.theta, rocky.x_test, rocky.mtest)
	accuracy = 0
	for col in range(len(cst.houses)):
		for row in range(rocky.mtest):
			if rocky.y_test[row, col] == 1 and output[row] == col:
				accuracy += 1

	accuracy = accuracy * 100 / rocky.mtest
	print("You got an accuracy of {:.2f}%".format(accuracy))

def save_thetas(theta, filename):
	with open(filename, 'wb') as fobj:
		pkl.dump(theta, fobj)

def main():
	args = parse.get_args_train()
	if args == -1:
		return
	df = parse.normalize_df(parse.read_file(args.fname_dataset))
	df1 = df.copy()[['Hogwarts House'] + cst.feat_list]
	df1 = df1.replace(np.nan, 0.5)
	rocky = Rocky(df1, tp=(59 if args.accuracy else 100))
	rocky.y = rocky.get_binary_house()
	rocky.gradient()
	save_thetas(rocky.theta, args.fname_weights)
	if args.accuracy:
		accuracy(rocky)

if __name__ == "__main__":
	main()

