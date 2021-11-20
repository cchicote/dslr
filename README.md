# DSLR
### Harry Potter et le datascientist
Codez un classifieur et sauvez Poudlard !

## Usage:
```
./describe.py		-f [dataset]
./histogram.py		-f [dataset]
./scatter_plot.py	-f [dataset]
./pair_plot.py		-f [dataset]

./logreg_train.py	-f [dataset] -w [weigts file] [-a]
./logreg_predict.py	-f [dataset] -w [weigts file]
```

## Dependencie:

We suppose you already install python3

### Linux
```
pip3 -> (sudo) apt install python3-pip
venv -> (sudo) apt-get install python3-venv
```
**check for update with apt-get update**

## Before running:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```