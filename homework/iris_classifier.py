# -*- coding: utf-8 -*-
import sys

from sklearn.datasets import load_iris

from sklearn.model_selection import train_test_split

import pandas as pd
from pandas.tools.plotting import scatter_matrix

import matplotlib.pyplot as plt
import numpy as np

import mglearn


def get_iris_dataset():
    iris_dataset = load_iris()

    #1. The format of the dataset
    print("Keys of iris_dataset: \n{}".format(iris_dataset.keys()))
    print("Target names: {}".format(iris_dataset['target_names']))
    print("Feature names: \n{}".format(iris_dataset['feature_names']))
    # data -> numpy.ndarray
    # row -> the labels
    # column -> the features
    print("Type of data: {}".format(iris_dataset['data'].shape))     # (150,4)
    print("Type of target: {}".format(iris_dataset['target'].shape)) # (150,)


    #2. split the dataset into training set and testing set
    X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)
    print("X_train shape: {}".format(X_train.shape))
    print("y_train shape: {}".format(y_train.shape))

    print("X_test shape: {}".format(X_test.shape))
    print("y_test shape: {}".format(y_test.shape))

    # 3. inspect the data
    # convert Numpy array int oa pandas DataFrame
    iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)

    # pdb; pdb.set_trace()
    grr = pd.scatter_matrix(iris_dataframe, c=y_train, figsize=(15,15), marker='o', hist_kwds={'bins':20}, s=60, alpha=.8, cmap=mglearn.cm3)
    #plt.show()


    # The modelu
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1)
    # build the model on the training set
    knn.fit(X_train, y_train)

    # the prediction
    X_new = np.array([[5, 2.9, 1, 0.2]])
    prediction = knn.predict(X_new)
    print("Prediction: {}".format(prediction))
    print("Predicted target name: {}".format(iris_dataset['target_names'][prediction]))

    y_pred = knn.predict(X_test)
    print("Test set predictions:\n {}".format(y_pred))
    print("Test set score: {:.2f}".format(np.mean(y_pred==y_test)))

if __name__ == '__main__':
    get_iris_dataset()
