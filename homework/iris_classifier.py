# -*- coding: utf-8 -*-

from sklearn.datasets import load_iris

from sklearn.model_selection import train_test_split

import pandas as pd
from pandas.tools.plotting import scatter_matrix

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
    grr = scatter_matrix(iris_dataframe, c=y_train, figsize=(15,15), marker='o', hist_kwds={'bins':20}, s=60, alpha=.8, cmap=mglearn.cm3)




if __name__ == '__main__':
    get_iris_dataset()
