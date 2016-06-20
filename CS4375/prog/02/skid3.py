'''sklearn id3'''
from sklearn.datasets import load_iris
from sklearn import tree
import itertools
from id3 import get_args, get_data

def id3():
    '''main program'''
    iris = load_iris()

    args = get_args()

    data = get_data(args, 1)
    test = get_data(args, 2)

    classes = data[0]
    data.remove(classes)
    test.remove(classes)


    data_col = [row[len(data[0])-1] for row in data]

    print('data', len(data[0]))

    for row in data:
        del row[len(data[0])-1]

    test_col = [row[len(test[0])-1] for row in test]

    print('test', len(test[0]))

    for row in test:
        del row[len(test[0])-1]

    for i in range(0, len(test_col)):
        if test_col[i] != data_col[i]:
            print('different')
            break

    #data = list(map(list, zip(*data)))

    #data_col = list(map(list, zip(*data_col)))

    #test = list(map(list, zip(*test)))

    #test_col = list(map(list, zip(*test_col)))

    '''
    print(classes)

    print(data_col)
    print(test_col)
    '''

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
