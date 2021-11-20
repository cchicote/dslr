#!dslr_env/bin/python3
import parse
import logreg_train as lt
import pickle as pkl
import pandas as pd
import constants as cst
import numpy as np

def load_thetas(filename):
	try:
		with open(filename, 'rb') as fobj:
			try:
				theta = pkl.load(fobj)
			except EOFError:
				print("Empty .pkl file, exiting program.")
				exit(1)
			except pkl.UnpicklingError:
				print("Invalid .pkl file, exiting program")
				exit(1)
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
		exit (1)
	df = parse.normalize_df(parse.read_file(args.fname_dataset, check_hog=False))
	df1 = df.copy()[cst.feat_list]
	df1 = df1.replace(np.nan, 0.5)
	theta = load_thetas(args.fname_weights)
	y_pred = lt.predict(theta, df1, df1.shape[0])
	print_in_file(y_pred)

if __name__ == "__main__":
	main()
