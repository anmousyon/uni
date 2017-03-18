'''
id3 algorithm
This program uses the id3 algorithm to build a decision tree
It stores the samples in a list of lists (emulates conventional matrix)
It stores the classes in a single list
It stores the tree in a dictionary
It goes through the dict recursively for the test
Data:
    classes in top row, separated by spaces
    samples separated by spaces, one sample for each row
Output:
    tree in 'depth-first'-like structure
    percentage correct -> correct/num_of_samples
'''

import sys
from math import log
from collections import defaultdict

def get_args():
    '''read args and return a list of strings'''
    return sys.argv

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

def get_data(args, arg_num):
    '''read in training and testing data'''
    #fill the matrix
    data_matrix = fill_data(args, arg_num)
    return data_matrix

def get_majority(data_matrix, classes, target_class):
    '''get the value in a column that is most common'''
    target_index = classes.index(target_class)
    frequency = get_freq(data_matrix, target_index)
    maximum = 0
    majority = ''
    for key in frequency.keys():
        if frequency[key] >= maximum:
            maximum = frequency[key]
            majority = key
    return majority

def get_freq(data_matrix, target_index):
    '''gets the frequency of each value'''
    col = [row[target_index] for row in data_matrix]
    frequency = defaultdict(lambda: 0)
    for val in col:
        frequency[val] += 1
    #print(frequency)
    return frequency

def get_entropy(data_matrix, classes, target_class):
    '''calculates the entropy of a certain target_class'''
    entropy = 0.0
    #get index of target class
    target_index = classes.index(target_class)
    #get frequency of each value
    frequency = get_freq(data_matrix, target_index)
    #calculate log value safely
    for freq in frequency.values():
        if freq:
            log_val = log(freq/len(data_matrix), 2)
        else:
            log_val = 0
        entropy += ((-freq)/len(data_matrix)) * log_val
    return entropy

def get_ig(data_matrix, classes, choice, target_class):
    '''calculates the information gain of a split on a class'''
    #get index of class (c)
    choice_index = classes.index(choice)
    #get frequency of each value
    frequency = get_freq(data_matrix, choice_index)
    sub_entropy = 0.0

    for val in frequency.keys():
        #print("freq of value", frequency[val])
        #print("number of value possible", sum(frequency.values()))
        val_prob = frequency[val] / sum(frequency.values())
        data_subset = [entry for entry in data_matrix if entry[choice_index] == val]
        #print(data_subset)
        sub_entropy += val_prob * get_entropy(data_subset, classes, target_class)

    info_gain = get_entropy(data_matrix, classes, target_class) - sub_entropy
    #print("info_gain", info_gain)

    return info_gain

def pick_class(data_matrix, classes, target_class):
    '''find the best class to use'''
    best = classes[0]
    max_gain = 0.0

    #calculate information gain for each class
    for choice in classes:
        if choice != target_class:
            gain = get_ig(data_matrix, classes, choice, target_class)
            if gain > max_gain:
                max_gain = gain
                best = choice

    print("class:", best, "ig", max_gain)

    return best

def get_vals(data_matrix, classes, choice):
    '''get the possible values of a class'''
    choice_index = classes.index(choice)
    vals = []
    #get all values in column
    for row in data_matrix:
        vals.append(row[choice_index])
    #remove all duplicates
    vals = list(set(vals))
    return vals

def get_ex(data_matrix, classes, best, val):
    '''get an example row'''
    ex = [[]]
    best_index = classes.index(best)
    for row in data_matrix:
        if row[best_index] == val:
            new_row = []
            for i in range(0, len(row)):
                if i != best_index:
                    new_row.append(row[i])
            ex.append(new_row)
    ex.remove([])
    return ex

def print_tree(row, rec, best, val):
    '''print out a row for the tree'''
    #print the leading spaces
    for _ in range(1, rec):
        sys.stdout.write('   ')

    #print the value
    if best is None:
        sys.stdout.write(row)
    #print out the branch
    else:
        sys.stdout.write('|' + best + " = " + val)
    print('')

def make_tree(data_matrix, classes, target_class, recursion):
    '''make a decision tree recursively'''
    recursion += 1
    data_matrix = data_matrix[:]
    vals = [row[classes.index(target_class)] for row in data_matrix]
    default = get_majority(data_matrix, classes, target_class)

    #if data_matrix is empty or the classes is empty, use the default
    if not data_matrix or (len(classes) - 1) <= 0:
        print_tree(default, recursion, None, None)
        return default

    #if the amount of vals in vals[0] = number of vals total, use vals[0]
    #if all records in class have the same value, return that class
    elif vals.count(vals[0]) == len(vals):
        print_tree(vals[0], recursion, None, None)
        return vals[0]

    #otherwise make a new subtree and add it to the tree
    else:
        #choose the best class
        best = pick_class(data_matrix, classes, target_class)
        #create a new decision tree using best class and empty dict
        tree = {best:{}}
        #make a new tree for each value in best class
        for val in get_vals(data_matrix, classes, target_class):
            print_tree(None, recursion, best, val)
            ex = get_ex(data_matrix, classes, best, val)

            new_classes = classes[:]
            new_classes.remove(best)
            subtree = make_tree(ex, new_classes, target_class, recursion)

            #add the subtree to the main tree
            tree[best][val] = subtree
    return tree

def run_test(row, classes, target_index, tree, key):
    '''test if decision tree is correct'''
    #get the next key
    if isinstance(tree, dict):
        key = list(tree.keys())[0]

    #find the index of specified key in classes list
    key_index = classes.index(key)

    #get the value in that row
    val = row[key_index]

    #check the value
    if not isinstance(tree, dict):
        if row[target_index] == tree:
            return 1
        else:
            return 0

    #recursively go down the tree
    else:
        tree = (tree.get(key)).get(val)
        correct = run_test(row, classes, target_index, tree, key)
        return correct

def test(args, classes, target_class, tree, correct):
    '''test the decision tree for accuracy'''
    test_matrix = get_data(args, 2)
    test_matrix.remove(test_matrix[0])
    target_index = classes.index(target_class)

    rows = 0
    correct = 0

    for row in test_matrix:
        correct += run_test(row, classes, target_index, tree, '')
        rows += 1

    percentage = (correct / rows) * 100
    print('Accuracy on test set (', rows, 'instances):', percentage, '%')

def main():
    '''read and print data'''
    #grab the args
    args = get_args()

    #read data
    data_matrix = get_data(args, 1)
    classes = data_matrix[0]
    data_matrix.remove(classes)

    #set target class
    target_class = 'class'

    #make the tree, print the tree, print percentage
    tree = make_tree(data_matrix, classes, target_class, 0)

    test(args, classes, target_class, tree, 0)

main()
