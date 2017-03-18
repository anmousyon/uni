'''k medois implementation in python'''
import sys
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import json

import kmedoids

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

def extract(data, col):
    '''
    extract a column from the data
    takes:
        nested list -> full dataset
        int -> column number
    returns:
        nested list -> dataset excluding extracted column
        list -> extracted column
    '''
    extracted = [row.pop(col) for row in data]
    return data, extracted

def encode(col):
    '''
    encodes a column
    takes:
        list -> column to encode
    returns:
        list -> encoded column
        dictionary -> encoder/decoder for the column
    '''
    unq = {}
    count = 0
    #maps each value in the column to a unique, incrementing integer
    for item in col:
        if item not in unq:
            unq[item] = count
            count += 1
    enc = [val for item in col for key, val in unq.items() if item == key]
    return enc, unq

def fit_encode(data):
    '''
    fit all columns, encode them and recombine them
    takes:
        nested list -> all data to encode
    returns:
        nested list -> all encoded data
        list of dictionaries -> an encoder/decoder for each column
    '''
    columns = len(data[0])
    encoders = []
    cols = []
    for _ in range(columns):
        data, col = extract(data, col=0)
        col, encoder = encode(col)
        cols.append(col)
        encoders.append(encoder)
    #transpose the list of columns
    data = list(map(list, zip(*cols)))
    return data

def main():
    '''do clustering'''
    args = get_args()
    data = get_data(args, 2)
    data, classes = extract(data, 0)
    #data = fit_encode(data)
    data = np.array(data)

    # distance matrix
    distance = pairwise_distances(data, metric='euclidean')

    # split into k clusters
    M, clusters = kmedoids.kMedoids(distance, int(args[1]))

    print('centers:')
    for point_idx in M:
        print(data[point_idx])

main()