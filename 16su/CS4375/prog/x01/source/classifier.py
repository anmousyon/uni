'''classify the search term using gnb classifier'''
import pickle
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cross_validation import cross_val_predict
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import ml_helpers

def classify(test, test_):
    '''
    make predictions on test data, check accuracy
    takes:
        list of dictionaries -> encoders/decoders for each column
        nested list -> test instances
        list -> classes for the test instances
        int -> target column
    '''
    with open('classifier.pickle', 'rb') as cfile:
        classifier = pickle.load(cfile)

    print('score:', classifier.score(test, test_))

    predicted = cross_val_predict(classifier, test, test_, cv=10)

    _, axis = plt.subplots()
    axis.scatter(test_, predicted)
    axis.plot([min(test_), max(test_)], [min(predicted), max(predicted)], 'k--', lw=4)
    x = np.linspace(*axis.get_xlim())
    axis.plot(x, x)
    axis.set_xlabel('Measured')
    axis.set_ylabel('Predicted')
    plt.show()

def fit(train, train_):
    '''
    fit the classifier to the list of lists
    takes:
        nested list -> training data instances
        list -> classes for training instances
    '''
    classifier = GradientBoostingRegressor()
    classifier.fit(train, train_)

    with open('classifier.pickle', 'wb') as cfile:
        pickle.dump(classifier, cfile)

def fit_classify():
    '''train the classifier on the database'''
    data = []
    with open('data.csv', newline='') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in data_reader:
            data.append(row)
    data, classes = ml_helpers.prep_data(data, target=(len(data[0])-1))
    train, test, train_, test_ = train_test_split(data, classes, test_size=0.15, random_state=42)
    fit(train, train_)
    classify(test, test_)

fit_classify()
