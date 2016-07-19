'''bayes classifier'''
import sys
from sklearn.naive_bayes import GaussianNB

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

def listsum(to_sum):
    '''get sum of list'''
    lsum = 0
    for i in to_sum:
        lsum = lsum + i
    return lsum

def bayes():
    '''classify'''
    args = get_args()
    train = get_data(args, 1)
    test = get_data(args, 2)

    classes = train[0]
    train.remove(classes)
    train = [[int(x) for x in row] for row in train]
    classes = test[0]
    test.remove(classes)
    test = [[int(x) for x in row] for row in test]

    train_col = [row[len(row)-1] for row in train]
    for row in train:
        del row[len(row)-1]

    test_col = [row[len(row)-1] for row in test]
    for row in test:
        del row[len(row)-1]

    train_cols = []
    for col in range(len(train[0])):
        train_cols.append([row[col] for row in train])

    test_cols = []
    for col in range(len(test[0])):
        test_cols.append([row[col] for row in test])

    nbayes = GaussianNB()

    for index, col in enumerate(train_cols):
        sumoflist = listsum(col)
        print(('P(A' + str(index) + '=x1)'), sumoflist/len(col))
        print(('P(A' + str(index) + '=x2)'), (1-(sumoflist/len(col))))

    for index, col in enumerate(train_cols):
        tran = [[x] for x in col]
        result = nbayes.fit(tran, train_col)
        result = nbayes.score(tran, train_col)
        print('P(A' + str(index) + '=x1|C1)', result)
        print('P(A' + str(index) + '=x2)|C2)', 1-result)


    nbayes.fit(train, train_col)

    nbayes.predict(test)
    print('Accuracy on training set ('+str(len(train))+' instances):', nbayes.score(train, train_col))
    print('Accuracy on test set ('+str(len(train))+' instances):', nbayes.score(test, test_col))

bayes()
