from sklearn import tree
import numpy as np
import csv
import pydotplus
from sklearn import linear_model
import matplotlib.pyplot as plt

# process data in Numpy array form
with open('resultlist.csv', 'r') as data_file:
    data_iter = csv.reader(data_file, delimiter=',')
    data = [data for data in data_iter]
    data_array = np.asarray(data)
    actual_array = np.asarray(data_array[1:,:], dtype=float)

    # use Decision Tree Classifier
    feature_row = data_array[0,:] # a list of features
    class_col = data_array[1:,12] # a column vector of classes
    X = data_array[1:,0:12]
    Y = class_col
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X,Y)

    # testing data
    t1 = [40, 10, 0, 500, 800, 1, 0, 1, 13, 300, 0, 2]
    print clf.predict([t1])
 
    # plot tree in tree.pdf
    dot_data = tree.export_graphviz(clf, out_file=None) 
    graph = pydotplus.graph_from_dot_data(dot_data) 
    graph.write_pdf("tree.pdf") 

    # use Generalized Linear Models
    reg = linear_model.LinearRegression()
    reg.fit(X,Y)
    print "Coefficients:" + reg.coef_
