import numpy as np
import matplotlib.pyplot as plt 
import math 
import csv 


def data_noisy_deletion(path):
    '''
    Noticed that some of the data lines is 
    'App msg queue full, see https://dev.fitbit.com/kb/message-queue-full for recommendations.'
    This warning is actually of no use... We can not segment data collection program into small
    pieces. Because if sensors rest for a while as they said in the above link, some data can not 
    be collected... 
        input:
            path: path of the file to adjust
    '''
    file_data = open(path, 'r')
    file_name = path.split('.')[0]
    output_file = open(file_name + '_deletion.txt', 'w')

    for line in file_data.readlines():
        if (line.split()[2].isalpha()):
            continue
        else:
            output_file.write(line) 

    output_file.close()
    file_data.close()


def txt_to_csv(path):
    '''
        To convert txt data into csv form. 
        There are 3 places in the txt file in this project to delete.
        They are [0],[1] and [-1] after spliting.
        Notice that there is also a comma at the end of each float data except 
        the [-2] one. 
    '''

    file_name = path.split('.')[0]

    with open(file_name + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
    
        with open(path, 'r') as filein:
            for line in filein:
                line_list = line.strip('\n').split()
                line_list.pop(0)
                line_list.pop(0)
                line_list.pop(-1)
                n = len(line_list)
                for i in range(n):
                    if (line_list[i][-1] == ','):
                        line_list[i] = float(line_list[i][:-1])
                    else:
                        line_list[i] = float(line_list[i])
                spamwriter.writerow(line_list)


    


def split_data_file(path, interval):
    '''
        input:
            path: path of file to split
            interval: split interval
        output:
            file_list: list of splited flie
    ''' 
    file_list = []
    file_data = open(path,'r')

    count = 1
    curr_file_period = []
    for line in file_data.readlines():
        curr_file_period.append(line)
        if(count % interval == 0):
            file_list.append(curr_file_period)
            curr_file_period = []
        count += 1
    if (len(curr_file_period)!=0):
        file_list.append(curr_file_period)

    return file_list

def extract_data(data_line):
    '''
    To extract data from row Fitbit console log output.
        input:
            data_line: input data line 
        output: 
            data tuple like (x_acc, y_acc, z_acc)
    '''
    line_list = data_line.split()
    x_acc = float(line_list[2][:-1])
    y_acc = float(line_list[3][:-1])
    z_acc = float(line_list[4])
    return (x_acc, y_acc, z_acc)

def cosine_distance(vector_1, vector_2):
    dot_product = sum(i*j for i, j in zip(vector_1, vector_2))
    modulus_1 = sum(i*j for i, j in zip(vector_1, vector_1)) 
    modulus_2 = sum(i*j for i, j in zip(vector_2, vector_2))
    
    return dot_product/(modulus_1*modulus_2)

def encode(data_tuple, codebook):
    '''
        input:
            data_tuple: data like (x_acc, y_acc, z_acc)
            codebook: code book and corresponding direction vector, in the form of a dict 
                a:(1,0,0)
                b:(0,1,0) 
                c:(0,0,1)
                d:(-1,0,0)
                e:(0,-1,0)
                f:(0,0,-1)
        output:
            encoded: string like 'a', 'b' or 'c'
    '''
    encoded_strings = list(codebook.keys())
    # encoded_strings = ['a','b','c','d','e','f']

    encode_tuples = list(codebook.values())
    # encode_tuples = [(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
    
    max_consine_distance = -float("inf")
    encoded = 'a' 
    for i in range(len(encode_tuples)):
        if(cosine_distance(data_tuple, encode_tuples[i])>max_consine_distance):
            max_consine_distance = cosine_distance(data_tuple, encode_tuples[i])
            encoded = encoded_strings[i]
    return encoded


def min_edit_distance(str_1, str_2, codebook):
    '''
    Using dynamic programming to compute the minimum edit distance between two strings, 
    here 
    input:
        str_1, str_2: strings that are going to be computed 
        codebook: code book and corresponding direction vector, in the form of a dict 
    output:
        min_distance: minimum edit distance, 
    '''
    # to get necessary value
    n = len(str_1)
    m = len(str_2)
    edit_distance_matrix = np.zeros((n,m))

    
    # initialization
    for i in range(n):
        # the formula of weighted edit distance is f(i,j) = exp(∠(vi,vj)/100) - 1  
        angle_in_degree = math.acos(cosine_distance(codebook[str_1[i]], codebook[str_2[0]]))*180/math.pi 
        # here deletion cost, insertion cost and substitution cost are computed from the same formula
        deletion_cost = math.exp(angle_in_degree / 100) - 1
        edit_distance_matrix[i, 0] = i * deletion_cost

    for i in range(m):
        angle_in_degree = math.acos(cosine_distance(codebook[str_1[0]], codebook[str_2[i]]))*180/math.pi 
        deletion_cost = math.exp(angle_in_degree / 100) - 1
        edit_distance_matrix[0, i] = i * deletion_cost

    for i in range(1,n):
        for j in range(1,m):
            angle_in_degree = math.acos(cosine_distance(codebook[str_1[i]], codebook[str_2[j]]))*180/math.pi
            deletion_cost = math.exp(angle_in_degree / 100) - 1
            edit_distance_matrix[i,j] = min(edit_distance_matrix[i-1,j]+deletion_cost, \
                edit_distance_matrix[i,j-1]+deletion_cost, edit_distance_matrix[i-1,j-1]+deletion_cost)
    
    return edit_distance_matrix[n-1,m-1]



txt_to_csv('data/snap/snap_1.txt')
