'''sklearn id3'''
import sys
from sklearn.datasets import load_iris
from sklearn import tree
#from id3 import get_args, get_data

def get_args():
    '''read args and return a list of strings'''
    return sys.argv

def get_data(args, arg_num):
    '''read in training and testing data'''
    #fill the matrix
    data_matrix = fill_data(args, arg_num)
    return data_matrix

def fill_data(args, arg_num):
    '''read in the data and return the matrix'''
    data_matrix = []

    with open(args[arg_num]) as data:
        for line in data:
            if line.split():
                row = []
                for word in line.split():
                    row.append(word)
                data_matrix.append(row)
    return data_matrix

def id3():
    '''main program'''
    args = get_args()

    data = get_data(args, 1)
    test = get_data(args, 2)

    classes = data[0]
    data.remove(classes)
    test.remove(classes)


    data_col = [row[len(data[0])-1] for row in data]

    for row in data:
        del row[len(data[0])-1]

    test_col = [row[len(test[0])-1] for row in test]

    for row in test:
        del row[len(test[0])-1]

    for i in range(0, len(test_col)):
        if test_col[i] != data_col[i]:
            print('different')
            break
    print(data)
    print(data_col)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data, data_col)

    correct = 0

    prediction = clf.predict(test)
    for i in range(0, len(test)-1):
        if prediction[i] == test_col[i]:
            correct += 1

    print(correct)
    print(len(test))
    print(correct/len(test))

    #print(prediction)


id3()
