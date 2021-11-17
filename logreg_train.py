#!dslr_env/bin/python3
import sys
import parse
import constants as cst
import numpy as np
import pandas as pd
import math

feat_list = ['Astronomy', 'Herbology', 'Ancient Runes']

def de_normalize(value, max_value, min_value):
		return value * (max_value - min_value)

class Rocky():
	def __init__(self, df, learningRate = 0.1, learningRateGoal = 0.0000001, precision = 10, it_max = 1000):
		self.df = df
		self.x = df.copy()[feat_list].to_numpy()				# shape = student * features
		self.m, self.n = self.x.shape							# len student, len features
		self.y = self.get_binary_house()						# shape = student * houses
		self.theta = np.zeros(shape=(self.n, len(cst.houses)))	# shape = features * houses
		self.thetas_hist = [self.theta.copy()]
		self.cost = self.n
		self.cost_hist = [self.n]
		self.it = 0
		self.it_max = it_max
		self.lr = learningRate
		self.lrGoal = learningRateGoal
		self.min_cost_diff = 10 ** -precision

	def get_binary_house(self):
		y = np.zeros([self.m, len(cst.houses)])
		house = self.df.copy()["Hogwarts House"].to_numpy()
		for i in range(self.m):
			y[i, cst.houses.index(house[i])] = 1

		return y

	def sigmoid(self, z):
		return 1.0 / (1 + np.exp(-z))

	def	get_cost(self):
		# print("============= COST ===============")

		pred = self.sigmoid(np.dot(self.x, self.theta))
		self.cost = -(1 / self.m) * np.sum(self.y * np.log(pred) + (1 - self.y) * np.log(1 - pred))

		tmp = self.cost
		self.cost_hist.append(tmp)
		# print("cost: ", self.cost)

	def update_theta(self, pred, house, feat):
		# print("============= UPDATE THETA ===============")
		
		dt = (1 / self.m) * np.sum((pred - self.y[:,house]) * self.x[:,feat])

		self.theta[feat, house] -= self.lr * dt
		
		self.thetas_hist.append(self.theta.copy())

	def	accuracy(self):
		output = self.predict()
		print("============= ACCURACY ===============")
		accuracy = 0
		l = 0
		for col in range(len(cst.houses)):
			for row in range(self.m):
				if self.y[row, col] == 1 and output[row] == col:
					accuracy += 1
				l+= 1

		accuracy = accuracy * 100 / self.m
		print(accuracy)

	def	predict(self):
		print("============= PREDICT ===============")
		output = []
		for house in range(len(cst.houses)):
			res = self.sigmoid(np.dot(self.theta[:, house], self.x.T))
			output.append(res)

		output = np.array(output)
		max = np.amax(output, axis=0)
		ret = []
		for i in range(self.m):
			bruh = np.where(output[:,i] == max[i])
			ret.append(bruh[0][0])

		return ret
	
	def gradient(self):
		for i in range(self.it_max):
			self.it += 1
			self.get_cost()
			for house in range(len(cst.houses)):
				pred = self.sigmoid(np.dot(self.x, self.theta[:, house].T))
				for feat in range(self.n):
					self.update_theta(pred, house, feat)
				if self.it > 10 and abs(self.cost - self.cost_hist[-2]) < self.min_cost_diff:
					print("BREAK COST")
					break
				if self.lr <= self.lrGoal:
					print("BREAK LR")
					break
				if self.cost > self.cost_hist[-2]:
					self.cost = self.cost_hist[-2]
					self.theta = self.thetas_hist[-2]
					self.lr /= 10
					print("new lr= ", self.lr)
			else:
				continue
			break
		print("============= THETA ===============  it= ", self.it)
		print(self.theta)
		self.accuracy()

def main():
	filename = parse.get_filename(sys.argv, len(sys.argv))
	df = parse.normalize_df(parse.read_file(filename))
	df1 = df.copy()[['Hogwarts House', 'Astronomy', 'Herbology', 'Ancient Runes']]
	df1.dropna(inplace=True)
	# print(df['Hogwarts House'])
	rocky = Rocky(df1)
	rocky.gradient()


if __name__ == "__main__":
	main()



# class Rocky():
# 	def __init__(self, df, learningRate = 0.01, learningRateGoal = 0.0000001, precision = 15):
# 		self.df = df
# 		self.x = df.copy()[feat_list].to_numpy()
# 		self.m, self.n = self.x.shape
# 		self.y = []
# 		self.pred = []
# 		self.theta = np.zeros((self.n,1))
# 		self.dt = self.theta.copy()
# 		self.bias = 0
# 		self.final_theta = {key: [] for key in cst.houses}
# 		self.learningRate = learningRate
# 		self.learningRateGoal = learningRateGoal
# 		self.min_cost_diff = 10 ** -precision

# 	def is_from_house(self, house):
# 		return np.where(self.df['Hogwarts House'] == house, 1, 0)

# 	# only for predict
# 	def sigmoid(self, theta, x):
# 		z = np.dot(x, theta) + self.bias
# 		return 1.0 / (1 + np.exp(-z))

# 	# get the cost with the lastest thethas
# 	def get_new_cost(self, pred):
# 		self.cost = (-1 / self.m) * np.sum(np.dot(self.y, np.log(pred)) + np.dot((1 - self.y), np.log(1 - pred)))

# 	# fct for get thetas and the derivate
# 	def update_theta(self, pred):
# 		self.dt = (1 / self.m) * np.dot((pred - self.y).T, self.x)
# 		dt_bias = (1 / self.m) * np.mean(pred - self.y)

# 		test = self.learningRate * self.dt
# 		print(test.shape)
# 		self.theta -= test
# 		self.bias -= self.learningRate * dt_bias

# 	# loop of training
# 	def gradient(self):
# 		house = "Gryffindor"
# 		self.y = np.array([self.is_from_house(house)])
# 		self.theta = np.zeros(self.n)
# 		self.dt = self.theta.copy()
# 		self.bias = 0
# 		self.cost = np.zeros(self.n)
# 		for i in range(500):
# 			self.pred = self.sigmoid(self.theta, self.x)
# 			self.get_new_cost(self.pred)
# 			self.update_theta(self.pred)
# 		self.predict()

# 	def predict(self):
# 		print("===================== PREEDICT =================")
# 		for i in range(1):
# 			res = np.around(self.sigmoid(self.theta, self.x))
# 			for x in range(20):
# 				print(self.y[0,x], " - ", res[x])


# def logistic_regression(features, target, num_steps, learning_rate, add_intercept = False):
#     if add_intercept:
#         intercept = np.ones((features.shape[0], 1))
#         features = np.hstack((intercept, features))
        
#     weights = np.zeros(features.shape[1])
    
#     for step in xrange(num_steps):
#         scores = np.dot(features, weights)
#         predictions = sigmoid(scores)

#         # Update weights with gradient
#         output_error_signal = target - predictions
#         gradient = np.dot(features.T, output_error_signal)
#         weights += learning_rate * gradient
        
#         # Print log-likelihood every so often
#         if step % 10000 == 0:
#             print log_likelihood(features, target, weights)
        
#     return weights








	# # loop of training
	# def gradient(self):
	# 	#for house in cst.houses:
	# 	house = "Gryffindor"
	# 	for i in range(1):
	# 		self.y = np.array([self.is_from_house(house)])
	# 		self.theta = np.array(self.n * [np.zeros(1)])
	# 		self.dt = self.theta.copy()
	# 		self.bias = 0
	# 		self.cost = np.array(self.n * [np.zeros(1)])
	# 		for i in range(500):
	# 			self.pred = self.sigmoid(self.theta, self.x)
	# 			self.get_new_cost(self.pred)
	# 			self.update_theta(self.pred)

	# 		self.final_theta[house] = self.theta
	# 	self.predict()