'''testing differnt ml algs'''
import sys
import os.path
import collections
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split

ALGORITHMS = {
    'k-nearest neighbors' : KNeighborsClassifier(),
    'bagging' : BaggingClassifier(),
    'random forests' : RandomForestClassifier(),
    'adaboost' : AdaBoostClassifier(),
    'gradient boosting' : GradientBoostingClassifier()
}

ALGORITHMS = collections.OrderedDict(sorted(ALGORITHMS.items()))

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
                    row.append(float(word))
                data_matrix.append(row)
    return data_matrix

def check(prediction, test_data, test_col):
    '''check percentage of correct for prediction'''
    correct = 0
    for i in range(0, len(test_data)-1):
        if prediction[i] == test_col[i]:
            correct += 1
    return correct/len(test_data)

def write_table(table):
    '''write table to results file'''
    with open("results.txt", "a") as results:
        for item in table:
            results.write("%s\n" % item)

def add_to_list(results_table, dataset, size, split, accuracy):
    '''add new row to the table'''
    row = [dataset, size[0], size[1], split]
    for acc in accuracy:
        row.append(acc)
    results_table.append(row)
    return results_table

def results_header(results_table, algs):
    '''create heder for table'''
    header = ["dataset", "instances", "attributes", "split"]
    for alg in algs:
        header.append(alg)
    return header

def main():
    '''test all algs'''

    algs = ALGORITHMS.keys()

    results_table = []
    if not os.path.exists("results.txt"):
        results_table.append(results_header(results_table, algs))

    args = get_args()
    train_data = get_data(args, 1)

    train_col = [row[len(row)-1] for row in train_data]
    for row in train_data:
        del row[len(row)-1]

    train, test, train_result, test_result = train_test_split(
        train_data,
        train_col,
        test_size=0.2
        )

    dataset = [train, train_result, test, test_result]
    acc = []

    for alg in ALGORITHMS.values():
        #print(alg)
        model = alg
        model.fit(dataset[0], dataset[1])
        result = model.predict(dataset[2])
        #print(result)

        accuracy = check(result, dataset[2], dataset[3])
        accuracy *= 100000
        accuracy = float(int(accuracy))
        accuracy /= 100000
        acc.append(accuracy)

    results_table = add_to_list(
        results_table,
        args[1],
        [len(train_data), len(train_data[0])],
        "80/20",
        acc
        )
    write_table(results_table)

main()
