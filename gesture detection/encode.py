import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import os 

import preprocess as pre

move_period = 5
frequency = 50 # sampling frequency is 50 
interval = move_period * frequency 

#file_list = cd.split_data_file(file_path, interval)

codebook = {'a':(1,0,0),'b':(0,1,0),'c':(0,0,1),'d':(-1,0,0),'e':(0,-1,0),'f':(0,0,-1)}
encoded_list = []

file_path = 'data/applause'
files = os.listdir(file_path)

# encode all data in one file
for data_file in files:
    # if the current item is a direction then continue
    if (os.path.isdir(data_file)):
        continue
    # all data are in the form of txt, if not then continue
    if (not os.path.splitext(file_path + '/' + data_file)[-1] == '.txt'):
        continue
    if(not 'applause' in os.path.splitext(data_file)[0] ):
        continue
    file_list = pre.split_data_file(file_path + '/' + data_file, interval)
    for movement_data in file_list:
        curr_movement_data_list = []
        for data_line in movement_data:
            data_tuple = pre.extract_data(data_line)
            data_tuple = pre.encode(data_tuple, codebook)
            curr_movement_data_list.append(data_tuple)

        encoded_list.append(''.join(curr_movement_data_list))
#print(encoded_list)
# according to the paper, training is divided into 2-step
# the first step is the choose the movement string template, which is the string 
# has the lowest minimum edit distance between all other strings... so the time complexity
# of the first step will be O(n2), n is the size of all training data...
# also no adaptive changing during training...


movement_template = encoded_list[0]
total_min_edit_distance = float('inf')

encoded_list_length = len(encoded_list)

for i in range(encoded_list_length):
    curr_min_edit_distance = 0
    print("now on", i)
    for j in range(encoded_list_length):
        curr_min_edit_distance += pre.min_edit_distance(encoded_list[i], encoded_list[j], codebook)
    if (curr_min_edit_distance < total_min_edit_distance):
        total_min_edit_distance = curr_min_edit_distance
        movement_template = encoded_list[i]


template_file = open('data/applause/template.txt', 'w')

template_file.write(movement_template)

template_file.close()



