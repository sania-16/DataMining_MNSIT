# -*- coding: utf-8 -*-
"""mnsit_knn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IqvXdFxV6FSx2vSZ0zZHVYm_SYHKlD9w
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
#from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler
import numpy as np
import urllib.request
import gzip

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

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train.astype(np.float32))
X_test = scaler.transform(X_test.astype(np.float32))

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print("Accuracy_knn:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

cv_scores = cross_val_score(knn, X_train, y_train, cv=5)
print("Cross-validation scores:", cv_scores)
print("Mean cross-validation score:", cv_scores.mean())

params = {
    'n_neighbors': [3, 5, 7],
    'weights': ['uniform', 'distance']
}
grid_search = GridSearchCV(knn, params, cv=5)
grid_search.fit(X_train, y_train)
print("Best parameters:", grid_search.best_params_)
print("Best score:", grid_search.best_score_)
best_model = grid_search.best_estimator_
best_model.fit(X_train,y_train)
y_pred = best_model.predict(X_test)
print("Accuracy_grid:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

# Use randomized search to tune hyperparameters
params = {
    'n_neighbors': range(1, 31),
    'weights': ['uniform', 'distance'],
    'leaf_size': range(10, 101, 10)
}
random_search = RandomizedSearchCV(knn, params, n_iter=10, cv=5, scoring='accuracy')
random_search.fit(X_train, y_train)
print("Best parameters:", random_search.best_params_)
print("Best score:", random_search.best_score_)

# Train the model with the best hyperparameters
best_model = random_search.best_estimator_
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)
# Evaluate the performance of the model using different evaluation metrics
print("Accuracy_randon_search:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))