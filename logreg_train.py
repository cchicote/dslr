#!dslr_env/bin/python3
import sys
import parse
import constants as cst
import numpy as np
import pandas as pd
import math

feat_list = ['Astronomy', 'Herbology', 'Ancient Runes', 'Defense Against the Dark Arts']

class Rocky():
	def __init__(self, df, learningRate = 0.1, learningRateGoal = 0.0000001, precision = 15):
		self.df = df
		self.x = df.copy()[feat_list].to_numpy()
		self.m, self.n = self.x.shape
		self.y = []
		self.theta = np.array(self.n * [np.zeros(1)])
		self.dt = np.array(self.n * [np.zeros(1)])
		self.final_theta = {key: [] for key in cst.houses}
		self.cost = np.array(self.n * [np.zeros(1)])
		self.learningRate = learningRate
		self.learningRateGoal = learningRateGoal
		self.min_cost_diff = 10 ** -precision

	def is_from_house(self, house):
		return np.where(self.df['Hogwarts House'] == house, 1, 0)

	# only for predict
	def sigmoid(self, theta, x):
		return 1 / (1 + math.e ** -(theta.T * x))

	# fct for get thetas and the derivate
	def update_theta(self, pred):
		#self.dt = (1 / self.m) * sum((pred - self.y) * self.x)
		print("P", pred.shape)
		print("Y", self.y.shape)
		self.dt = np.dot(self.x.T, (pred - self.y))

		#self.theta -= self.learningRate * self.dt
		print("A", self.theta.shape)
		print("B", (self.learningRate * self.dt).shape)
		self.theta -= self.learningRate * self.dt

		# self.theta_hist.append(self.theta.copy())
		# self.dt_hist.append(self.dt.copy())

	# get the cost with the lastest thethas
	def get_new_cost(self, pred):
		#self.cost = - (1 / (2 * self.m)) * \
	#		sum(self.y * np.log(pred) + \
	#		(1 - self.y) * np.log(1 - pred))

		# print(self.y.shape)
		# print(pred.shape)
		self.cost = np.dot(-(1 / (2 * self.m)), np.sum(np.dot(self.y, np.log(pred))) + np.dot((1 - self.y), np.log(1 - pred)))
		print("Cost", self.cost.shape)
		# self.cost_hist.append(self.cost.copy())

	# loop of training
	def gradient(self):
		for house in cst.houses:
			print("----- " + house + " -----")
			# self.__init__(self.df)
			self.y = np.array([self.is_from_house(house)])
			print(self.y)
			while self.learningRate > self.learningRateGoal:
				curr_pred = self.sigmoid(self.theta, self.x)
				self.get_new_cost(curr_pred)
				self.update_theta(curr_pred)
				# if abs(self.cost - self.cost_hist[-2]) < self.min_cost_diff:
				# 	break
				# if self.cost > self.cost_hist[-2]:
				# 	self.cost = self.cost_hist[-2]
				# 	self.theta = self.theta_hist[-2]
				# 	self.learningRate /= 10

			self.final_theta[house] = self.theta
		print(self.final_theta)

def main():
	filename = parse.get_filename(sys.argv, len(sys.argv))
	df = parse.normalize_df(parse.read_file(filename))
	feat_list = ['Astronomy', 'Herbology', 'Ancient Runes', 'Defense Against the Dark Arts']
	# for feature in feat_list:
	#df1 = df.copy()[['Hogwarts House', feat_list]]
	df1 = df.copy()[['Hogwarts House', 'Astronomy', 'Herbology', 'Ancient Runes', 'Defense Against the Dark Arts']]
	df1.dropna(inplace=True)
	rocky = Rocky(df1)
	rocky.gradient()
	#print(df1)

if __name__ == "__main__":
	main()
