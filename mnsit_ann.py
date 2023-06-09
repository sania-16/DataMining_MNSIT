# -*- coding: utf-8 -*-
"""MNSIT_ANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12cIPePGgssaBMVoq85Fq04kVIZnNZEGp
"""

import urllib.request
import gzip
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import randint
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

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

# Create an ANN classifier
ann_clf = MLPClassifier()
ann_clf.fit(X_train, y_train)
y_pred = ann_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy_ann_clf: ', accuracy)
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

# Define the hyperparameters for grid search
param_grid = {
    'hidden_layer_sizes': [(100,), (100, 50), (50,)],
    'activation': ['relu', 'tanh', 'logistic'],
    'solver': ['adam', 'sgd'],
    'alpha': [0.0001, 0.001, 0.01]
}

# Perform grid search with cross-validation
grid_search = GridSearchCV(ann_clf, param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Print the best hyperparameters and score
print('Best Hyperparameters: ', grid_search.best_params_)
print('Best Score: ', grid_search.best_score_)
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Calculate the evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy_grid: ', accuracy)
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))


# Create an ANN classifier with best hyperparameters
ann_clf = MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', alpha=0.0001)

# Evaluate the ANN classifier using k-fold cross-validation
scores = cross_val_score(ann_clf, X_train, y_train, cv=5, n_jobs=-1)
# Print the cross-validation scores
print('Cross-Validation Scores: ', scores)
ann_clf.fit(X_train,y_train)

# Make predictions on the test set
y_pred = ann_clf.predict(X_test)

# Calculate the evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy of best: ', accuracy)
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))