#!dslr_env/bin/python3
import parse
import logreg_train as lt
import pickle as pkl
import pandas as pd
import constants as cst
import numpy as np

feat_list = ['Astronomy', 'Herbology', 'Ancient Runes', 'Defense Against the Dark Arts', 'Divination', 'Transfiguration']

def load_thetas(filename):
	try:
		with open(filename, 'rb') as fobj:
			theta = pkl.load(fobj)
		return theta
	except IOError as e:
		print("Retrieve theta issue: %s" % (e))

def	print_in_file(y_pred):
	for i in range(len(y_pred)):
		y_pred[i] = cst.houses[y_pred[i]]
	
	y_pred_out = pd.DataFrame(y_pred)
	y_pred_out.columns = ["Hogwarts House"]
	y_pred_out.to_csv("houses.csv", index_label="Index")

# Lire fichier dataset_test.csv
# Output dans houses.csv au format Index,Hogwarts House
def main():
	args = parse.get_args_predict()
	if args == -1:
		return
	df = parse.normalize_df(parse.read_file(args.fname_dataset))
	df1 = df.copy()[feat_list]
	df1 = df1.replace(np.nan, 0.5)
	theta = load_thetas(args.fname_weights)
	y_pred = lt.predict(theta, df1, df1.shape[0])
	print_in_file(y_pred)

if __name__ == "__main__":
	main()
