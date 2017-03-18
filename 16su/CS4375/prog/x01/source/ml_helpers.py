'''helpers for the classifier'''

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

def prep_data(data, target):
    '''
    clean up and format data then get classes list
    takes:
        nested list -> data to prep
        int -> target column
    returns:
        nested list -> encoded data
        list -> column from the data
        list of dictionaries -> encoders/decoders for the data
    '''
    data, classes = extract(data, target)
    classes = list(map(int, classes))
    data = fit_encode(data)
    return data, classes
