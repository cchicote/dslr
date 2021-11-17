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
	def __init__(self, df, learningRate = 0.1, learningRateGoal = 0.0000001, precision = 15):
		self.df = df
		self.x = df.copy()[feat_list].to_numpy()
		self.m, self.n = self.x.shape
		self.y = []
		self.pred = []
		self.theta = np.zeros((self.n,1))
		self.dt = self.theta.copy()
		self.bias = 0
		self.final_theta = {key: [] for key in cst.houses}
		self.learningRate = learningRate
		self.learningRateGoal = learningRateGoal
		self.min_cost_diff = 10 ** -precision
		#self.min_x = []
		#self.max_x = []

	def is_from_house(self, house):
		return np.where(self.df['Hogwarts House'] == house, 1, 0)

	# only for predict
	def sigmoid(self, theta, x):
		# print("dim t.T * x: ", np.dot(x, theta.T).shape)
		# print("dim bias: ", self.bias.shape)
		z = np.dot(x, theta) + self.bias
		return 1.0 / (1 + np.exp(-z))

	def	loss(self):
		loss = -np.mean(np.dot(self.y), np.log(self.pred)) - np.dot((1 - self.y), np.log(1 - self.pred))
		return loss

	# get the cost with the lastest thethas
	def get_new_cost(self, pred):
		# print("============= COST ===============")
		# print("y: ", self.y.shape)
		# print("pred: ", pred.shape)
		# print("First: ", -(1 / self.m))
		# print("Second ", np.sum(np.dot(self.y, np.log(pred))))
		# print("Third: ", np.dot((1 - self.y), np.log(1 - pred)))
		# print("Fourth: ", np.sum(np.dot(self.y, np.log(pred)) + np.dot((1 - self.y), np.log(1 - pred))))
		self.cost = np.dot((-1 / self.m), np.sum(np.dot(self.y, np.log(pred)) + np.dot((1 - self.y), np.log(1 - pred))))
		# print("Cost: ", self.cost)

	# fct for get thetas and the derivate
	def update_theta(self, pred):
		# print("============= UPDATE THETA ===============")
		# print("1/m: ", (1 / self.m))
		# print("dim x.T: ", self.x.T.shape)
		# print("dim pred: ", pred.shape)
		# print("dim y.T: ", self.y.T.shape)
		# print("dot prod: ", np.dot(self.x.T, (pred - self.y.T)))
		# print("dim dt: ", self.dt.shape)
		#self.dt = (1 / self.m) * np.dot(self.x.T, np.sum((pred - self.y.T)))
		self.dt = (1 / self.m) * np.sum(np.dot(self.x.T, (pred - self.y)))
		dt_bias = (1 / self.m) * np.sum((pred - self.y))

		# print("theta: ", self.theta.shape)
		# print("dt: ", self.dt.shape)
		self.theta -= self.learningRate * self.dt
		self.bias -= self.learningRate * dt_bias
		# print("theta: ", self.theta)

	

	# loop of training
	def gradient(self):
		for house in cst.houses:
			# print("----- " + house + " -----")
			self.y = np.array([self.is_from_house(house)])
			self.theta = np.array(self.n * [np.zeros(1)])
			self.dt = self.theta.copy()
			self.bias = 0
			self.cost = np.array(self.n * [np.zeros(1)])
			# print(self.y)
			for i in range(50):
			#while self.learningRate > self.learningRateGoal:
				self.pred = self.sigmoid(self.theta, self.x)
				self.get_new_cost(self.pred)
				self.update_theta(self.pred)
				#break

			self.final_theta[house] = self.theta
		# for key in self.final_theta.keys():
		# 	print(key)
		# 	print(self.final_theta[key])
		self.predict()

	def predict(self):
		bla = []
		for l in list(self.df.loc[:20,"Hogwarts House"]):
			bla.append(l[0])
		print(bla)
		result = {}
		for house in self.final_theta.keys():
			print("----- " + house + " -----")
			print(self.final_theta[house])
			res = self.sigmoid(self.final_theta[house], self.x)
			#print(res)
			#result = np.where(res >= 0.5, 1, 0)
			result[house] = []
			for r in res:
				if r >= 0.5:
					result[house].append(1)
				else:
					result[house].append(0)
			print(result[house][:20])
		
def main():
	filename = parse.get_filename(sys.argv, len(sys.argv))
	df = parse.normalize_df(parse.read_file(filename))
	print(df)
	df1 = df.copy()[['Hogwarts House', 'Astronomy', 'Herbology', 'Ancient Runes']]
	df1.dropna(inplace=True)
	rocky = Rocky(df1)
	rocky.gradient()


if __name__ == "__main__":
	main()
