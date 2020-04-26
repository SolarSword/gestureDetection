import os 
import sys
import pandas

import preprocess as pre 
from dtw import DTW
from dtw import cosine_cost

data_path = 'data'
training_data_dir = os.listdir(data_path) # dir 

testing_data_dir = training_data_dir

motion_period = 5 # 5s
frequency = 50 # 50Hz
period = motion_period * frequency

dtw = DTW()

'''
# for training part:
for file_dir in training_data_dir:
    label = file_dir
    sub_set_files = os.listdir(data_path + '/' + file_dir)
    
    dataset = []

    for single_file in sub_set_files:
        # print(single_file)
        dataset += pre.data_segmentation(data_path + '/' + file_dir + '/' + single_file, period, 2, 5)
        # # timestamp accel*3 gyro*3 orientation*4
        # here just use accel*3 for training 
    dtw.dtw_train(dataset, label, cosine_cost)

dtw.template_save('model7.npy')
'''


# for computing training accuracy part:
dtw.tamplate_load('model7.npy')
total_motion_samples = 0
total_right_prediction = 0
class_accuracy = []

tuple_record = []

postive = {'applause_twice':0, 'clockwise_circle':0, 'push':0, 'raise_arm':0, 'snap_a_finger_arm_down':0, 'snap_a_finger_arm_up':0, 'wave_down':0, 'None':0}
all_result = {'applause_twice':[], 'clockwise_circle':[], 'push':[], 'raise_arm':[], 'snap_a_finger_arm_down':[], 'snap_a_finger_arm_up':[], 'wave_down':[], 'None':[]}
for file_dir in testing_data_dir:
    label = file_dir
    sub_set_files = os.listdir(data_path + '/' + file_dir)
    right_prediciton = 0
    dataset = []

    for single_file in sub_set_files:
        # print(single_file)
        dataset += pre.data_segmentation(data_path + '/' + file_dir + '/' + single_file, period, 2, 5)
                 
    total_motion_samples += len(dataset)

    for i in range(0, len(dataset)):
        prediction_label = dtw.test(dataset[i], cosine_cost)
        all_result[label].append(prediction_label)
        postive[prediction_label] += 1
        if (prediction_label == label):
            right_prediciton += 1
            print('sample {} from {} is right'.format(i, label))
    
    tuple_record.append((label, right_prediciton, len(dataset)))

    class_accuracy.append((label, right_prediciton / len(dataset)))
    total_right_prediction += right_prediciton

print(class_accuracy)
print(tuple_record)
print(postive)
print(all_result)
print(total_right_prediction/total_motion_samples)



