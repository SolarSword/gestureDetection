import os 
import math 

import edit_distance as pre
template_file = open('data/applause/template.txt', 'r')
template = template_file.readline()



move_period = 5
frequency = 50 # sampling frequency is 50 
interval = move_period * frequency 

#file_list = cd.split_data_file(file_path, interval)

codebook = {'a':(1,0,0),'b':(0,1,0),'c':(0,0,1),'d':(-1,0,0),'e':(0,-1,0),'f':(0,0,-1)}
encoded_list = []

file_path = 'data/wave_down'
files = os.listdir(file_path)

# encode all data in one file
for data_file in files:
    # if the current item is a direction then continue
    if (os.path.isdir(data_file)):
        continue
    # all data are in the form of txt, if not then continue
    if (not os.path.splitext(file_path + '/' + data_file)[-1] == '.txt'):
        continue
    if(not 'wave_down' in os.path.splitext(data_file)[0] ):
        continue

    file_list = pre.split_data_file(file_path + '/' + data_file, interval)
    for movement_data in file_list:
        curr_movement_data_list = []
        for data_line in movement_data:
            data_tuple = pre.extract_data(data_line)
            data_tuple = pre.encode(data_tuple, codebook)
            curr_movement_data_list.append(data_tuple)

        encoded_list.append(''.join(curr_movement_data_list))


# to compute the mean edit distance of this template on the training data set 
sum_edit_distance = 0
for string in encoded_list:
    sum_edit_distance += pre.min_edit_distance(template, string, codebook)

mean = sum_edit_distance/len(encoded_list)

# to compute the standard deviation
sum_edit_square = 0
for string in encoded_list:
    sum_edit_square += (pre.min_edit_distance(template, string, codebook) - mean)**2

deviation = math.sqrt(sum_edit_square / len(encoded_list))

print(mean)
print(deviation)