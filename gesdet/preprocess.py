'''
    This program file is mainly designed to implement data segmentation
'''
import pandas as pd 
import numpy as np
import csv 
from vector import Vector
import math

def cosine_cost(vector_1, vector_2):
    
    return math.acos(round(vector_1.dot(vector_2)/(vector_1.modulus() * vector_2.modulus()), 5))

def euclidean_cost(vector_1, vector_2):
    return (vector_1 - vector_2).modulus()

def data_segmentation(path, period, start = 0, end = None):
    '''
        input: 
            path: data file path
            period: segmentation period 
            start: start index of every item
            end: end index of every item
    '''
    
    df = pd.read_csv(path)
    data_list = np.array(df).tolist()
    data_list = list(map(lambda x: Vector(tuple(x[start:end])), data_list))
    # the segmentation should let each segment contain the motion data
    # but data collection is done by letting volunteer act every 5s
    # from 0s. So we had better 'release' some data from the beginning 
    # then start to do data segmentation.

    # Empirically speaking, we just need to release 2s' data
    # since sampling frquency is 50Hz, so it means around 100 lines 
    for i in range(0, 100):
        data_list.pop(0)

    # segmentation
    # every segmentation is a sublist of this 
    output_data_list = []
    curr_list = []
    length = len(data_list)
    for i in range(0, length):
        curr_list.append(data_list[i])

        if ((i+1) % period == 0):
            
            output_data_list.append(curr_list)
            curr_list = []
        
        if (i+1 == length and curr_list):
            
            output_data_list.append(curr_list)

    return output_data_list
            

def unification():
    pass

def labeling(data_sample, label):
    '''
        This function is used to label data samples from raw data.
        For example, if we have already gotten a data sample like:[element_1, element_2, ... , element_n],
        but this sample doesn't have a label. Then you can use this function to label it to get 
        (label, [element_1, element_2, ... , element_n]). This is easy for computing accuracy.
        ***Note***
        This is only for one single sample. You need to use a loop to call this function if you want to 
        label all the data samples in a dataset.
    '''
    return (label, data_sample)


def active_segmentation(path, distance_function, period, threshold, start = 0, end = None):
    '''
        To segment a data flow from a file according to the change of distances 
        between points. 
        input:
            path: the file path to be segmented 
            distance_function: the function being used to compute the distance between points
            period: the window size of a predefined 'thing'
            threshold: the threshold to examine whether the data within the  period is a defined 'thing'
            start: start index of a point, NOT THE START INDEX OF THE DATA FLOW  
            end: end index of point, NOT THE END INDEX OF THE DATA FLOW
        return:
            a list containing elements that are the predefined 'thing'
    '''
    df = pd.read_csv(path)
    data_list = np.array(df).tolist()
    data_list = list(map(lambda x: Vector(tuple(x[start:end])), data_list))

    data_length = len(data_list)
    window_front = 0
    window_end = window_front + period
    result = []
    
    while(True):
        
        # first to compute the sum of distance within a window
        curr_distance_sum = distance_sum(data_list[window_front:window_end], euclidean_cost)
        if (curr_distance_sum >= threshold):
            # in this case, we view it as a predifined 'thing'
            # actually, specifically speaking, we view it as a motion data flow  
            result.append(data_list[window_front:window_end])
            window_front += period
            window_end = window_front + period
        else:
            window_front += 1
            window_end += 1

        if (window_end >= data_length):
            break 
        

    return result

def distance_sum(data_list, distance_function):
    distance_sum = 0
    data_length = len(data_list)
    for i in range(1, data_length):
        distance_sum += distance_function(data_list[i-1], data_list[i])

    return distance_sum 
     
'''
path = 'data/applause_twice/applause_twice_1_.csv'


#df = pd.read_csv(path)
#data_list = np.array(df).tolist()
#data_list = list(map(lambda x: Vector(tuple(x[2:5])), data_list))

#print(distance_sum(data_list[450:551], euclidean_cost))

segments = data_segmentation(path, 250 ,2, 5)
#segments = active_segmentation(path, euclidean_cost, 100, 200, 2, 5)
print(len(segments))
import matplotlib.pyplot as plt

for i in range(0, len(segments)):
    segment = segments[i]

    x_axis = list(range(len(segment)))

    accel = list(map(lambda a : math.sqrt(a.value[0]**2 + a.value[1]**2 + a.value[2]**2) , segment))

    plt.plot(x_axis, accel)
    plt.show()
'''