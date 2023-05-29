# -*- coding: utf-8 -*-
"""mnsit_naive_bayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WSE0HwcXAg5ZNCFytqjUPomItD4r7M_N
"""

import urllib.request
import gzip
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

url = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
filename, headers = urllib.request.urlretrieve(url, 'train-images-idx3-ubyte.gz')
# Load training images
with gzip.open(filename, 'rb') as f:
    data = np.frombuffer(f.read(), np.uint8, offset=16)
    X_train = data.reshape(-1, 28*28)

url = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'
filename, headers = urllib.request.urlretrieve(url, 'train-labels-idx1-ubyte.gz')
# Load training labels
with gzip.open(filename, 'rb') as f:
    data = np.frombuffer(f.read(), np.uint8, offset=8)
    y_train = data

url = 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'
filename, headers = urllib.request.urlretrieve(url, 't10k-images-idx3-ubyte.gz')
# Load test images
with gzip.open(filename, 'rb') as f:
    data = np.frombuffer(f.read(), np.uint8, offset=16)
    X_test = data.reshape(-1, 28*28)

url = 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
filename, headers = urllib.request.urlretrieve(url, 't10k-labels-idx1-ubyte.gz')
# Load test labels
with gzip.open(filename, 'rb') as f:
    data = np.frombuffer(f.read(), np.uint8, offset=8)
    y_test = data

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)

nb = MultinomialNB()
nb.fit(X_train, y_train)
y_pred =nb.predict(X_test)
print('Accuracy_nb:', accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

pipe = Pipeline([('scaler', MinMaxScaler()), ('nb', nb)])
params = {'nb__alpha': [0.95, 0.97, 0.99, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 1.5, 2.0]}
grid = GridSearchCV(pipe, param_grid=params, cv=5)
grid.fit(X_train, y_train)
print('Best Parameters:', grid.best_params_)
print('Best Score:', grid.best_score_)
#best_params=grid.best_score_
y_pred = grid.predict(X_test)
print('Accuracy_grid:', accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

nbc=grid.best_estimator_
y_pred =nbc.predict(X_test)
print('Accuracy_nbc:', accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))