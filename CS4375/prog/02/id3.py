import sys
import os
from math import log
from collections import Counter
from collections import defaultdict

def get_args():
    '''read args and return a list of strings'''
    return sys.argv

def fill_data(args, arg_num):
    '''read in the data and return the matrix'''
    data_matrix = []

    with open(args[arg_num]) as data:
        #to skip the classes when reading in
        seen_classes = 0

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
        if frequency[key] > maximum:
            maximum = frequency[key]
            majority = key
    return majority

def get_freq(data_matrix, target_index):
    '''gets the frequency of each value'''
    col = [row[target_index] for row in data_matrix]
    frequency = defaultdict(lambda: 0)
    for val in col:
        frequency[val] += 1
    return frequency

def get_entropy(data_matrix, classes, target_class):
    '''calculates the entropy of a certain target_class'''
    entropy = 0.0
    #get index of target class
    #print(classes)
    target_index = classes.index(target_class)
    #get frequency of each value
    frequency = get_freq(data_matrix, target_index)
    #calculate log value safely
    for freq in frequency.values():
        if freq:
            log_val = log(freq/len(data_matrix), 2)
        else:
            log_val = 0
        entropy += (-freq/len(data_matrix)) * log_val
    return entropy

def get_ig(data_matrix, classes, choice, target_class):
    '''calculates the information gain of a split on a class'''
    #get index of class (c)
    c_index = classes.index(choice)
    #get frequency of each value
    frequency = get_freq(data_matrix, c_index)
    sub_entropy = 0.0

    for val in frequency.keys():
        val_prob = frequency[val] / sum(frequency.values())
        data_subset = [entry for entry in data_matrix if entry[c_index] == val]
        sub_entropy += val_prob * get_entropy(data_subset, classes, target_class)

    info_gain = get_entropy(data_matrix, classes, target_class) - sub_entropy

    return info_gain

def pick_class(data_matrix, classes, target_class):
    '''find the best class to use'''
    best = classes[0]
    max_gain = 0.0
    for choice in classes:
        if choice != target_class:
            gain = get_ig(data_matrix, classes, choice, target_class)
            if gain > max_gain:
                max_gain = gain
                best = choice
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

def make_tree(data_matrix, classes, target_class, recursion):
    '''make a decision tree recursively'''
    recursion += 1
    vals = [row[classes.index(target_class)] for row in data_matrix]
    default = get_majority(data_matrix, classes, target_class)
    data_matrix = data_matrix[:]

    #if data_matrix is empty or the classes is empty, use the default
    if not data_matrix or (len(classes) - 1) <= 0:
        return default

    #if the amount of vals in vals[0] = number of vals total, use vals[0]
    #if all records in class have the same value, return that class
    elif vals.count(vals[0]) == len(vals):
        return vals[0]

    #otherwise make a new subtree and add it to the tree
    else:
        #choose the best class
        best = pick_class(data_matrix, classes, target_class)
        #create a new decision tree using best class and empty dict
        tree = {best:{}}
        #make a new tree for each value in best class
        for val in get_vals(data_matrix, classes, target_class):
            for _ in range(1, recursion):
                sys.stdout.write('  ')
            sys.stdout.write('|' + best)
            print('')
            ex = get_ex(data_matrix, classes, best, val)
            new_classes = classes[:]
            new_classes.remove(best)
            subtree = make_tree(ex, new_classes, target_class, recursion)
            #add the subtree to the main tree
            tree[best][val] = subtree

    return tree
'''
def make_tree(data_matrix, classes, target_class, current_root):
    if current_root is None:
        new_root = pick_class(data_matrix, classes, target_class)
        print('new root found', new_root)
        make_tree(data_matrix, classes, target_class, new_root)
    else:
        vals = get_vals(data_matrix, classes, current_root)
        for val in vals:
            print('\t', current_root)
            #check for uniform decision?
            next_root = pick_class(data_matrix, classes, current_root)
            for row in data_matrix:
                del row[classes.index(current_root)]
            classes.remove(current_root)
            make_tree(data_matrix, classes, target_class, next_root)
'''

def test(args, tree):
    '''test the decision tree for accuracy'''
    test_matrix = get_data(args, 0)
    test_matrix.remove(test_matrix[0])

def main():
    '''read and print data'''
    #grab the args
    args = get_args()

    #read data and make trees
    data_matrix = get_data(args, 0)
    classes = data_matrix[0]
    data_matrix.remove(classes)
    target_class = 'class'
    tree = make_tree(data_matrix, classes, target_class, 0)
    test(args, tree)
main()
