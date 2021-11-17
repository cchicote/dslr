#!dslr_env/bin/python3
import sys
import parse
import constants as cst
import numpy as np
import pandas as pd
import math

feat_list = ['Astronomy'] #, 'Herbology', 'Ancient Runes'

def de_normalize(value, max_value, min_value):
		return value * (max_value - min_value)

class Rocky():
	def __init__(self, df, learningRate = 0.01, learningRateGoal = 0.0000001, precision = 15, it_max = 500):
		self.df = df
		self.x = df.copy()[feat_list].to_numpy()
		self.m, self.n = self.x.shape
		self.y = self.is_from_house()
		self.theta = np.zeros(shape=(len(cst.houses)))
		self.cost = 0
		self.it_max = it_max
		self.lr = learningRate

	def is_from_house(self):
		y = np.zeros([self.m, len(cst.houses)])
		house = self.df.copy()["Hogwarts House"].to_numpy()
		for i in range(self.m):
			y[i, cst.houses.index(house[i])] = 1

		return y

	def sigmoid(self, z):
		return 1.0 / (1 + np.exp(-z))

	def	get_cost(self, pred):
		# print("============= COST ===============")
		# print("dim y: ", self.y.shape)
		# print("dim log(pred): ", np.log(pred).shape)
		# print("dim (1 - y): ", (1 - self.y).shape)
		# print("dim log(1 - pred): ", np.log(1 - pred).shape)

		self.cost = -(1 / self.m) * np.sum(self.y * np.log(pred) + (1 - self.y) * np.log(1 - pred))

	def update_theta(self, pred, house):
		# print("============= UPDATE THETA ===============")
		# print("dim pred: ", pred.shape)
		# print("dim y[:,house]: ", self.y[:,house].shape)
		# print("dim x: ", self.x.shape)
		
		dt = (1 / self.m) * np.sum((pred - self.y[:,house]) * self.x.T)

		self.theta[house] -= self.lr * dt

	def	accuracy(self):
		print("============= ACCURACY ===============")

	def	predict(self):
		print("============= PREDICT ===============")
		output = []
		for house in range(len(cst.houses)):
			res = np.around(self.sigmoid(np.dot(self.theta[house], self.x.T)))
			output.append(res)
		print(output)
	
	def gradient(self):
		for i in range(self.it_max):
			for house in range(len(cst.houses)):
				pred = self.sigmoid(np.dot(self.theta[house], self.x.T))
				# self.get_cost(pred)
				self.update_theta(pred, house)

		self.predict()

def main():
	filename = parse.get_filename(sys.argv, len(sys.argv))
	df = parse.normalize_df(parse.read_file(filename))
	df1 = df.copy()[['Hogwarts House', 'Astronomy']] #, 'Herbology'#, 'Ancient Runes'
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