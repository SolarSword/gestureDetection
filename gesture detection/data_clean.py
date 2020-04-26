'''
this program is mainly used to do the data clean 
data is collected from Fitbit Versa 
After many failed attempts, interpolation works 
well on my data set collecting and data cleaning
'''
import csv 
import pandas as pd 

row_data_path = 'test_data/test_2.csv'
accel = []
gyro = []
ori = []

with open(row_data_path) as sensor_data_file:
    sensor_data_file_csv = csv.reader(sensor_data_file)
    for line in sensor_data_file_csv:
        if(line == []):
            continue
        if(line[0] == '1'):
            accel.append((float(line[1]), float(line[2]), float(line[3]), float(line[4])))
        elif(line[0] == '2'):
            gyro.append((float(line[1]), float(line[2]), float(line[3]), float(line[4])))
        else:
            ori.append((float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])))
            

# after some observation... I found that the output of the sensors may 
# not in order... so we need to sort the data list by timestamp
def take_first(elem):
    return elem[0]

accel.sort(key = take_first)
gyro.sort(key = take_first)
ori.sort(key = take_first)


# generally speaking, acceleration list from accelerometer is the longest
# (maybe because the accelerometer is the most sensitive sensor)
# here we use the shorter list to fill in the longer list
# that is to say the length of the output list (to converted to csv later) 
# is the same as the longest list in the raw data 

output = []

gyro_idx = 0
ori_idx = 0

gyro_len = len(gyro) - 1
ori_len = len(ori) - 1

for i in range(len(accel)):
    if(accel[i][0] < gyro[gyro_idx][0] and gyro_idx == 0):
        pass 
    elif(gyro_idx == gyro_len):
        pass 
    else:
        while(not (gyro[gyro_idx][0] <= accel[i][0] and accel[i][0] < gyro[gyro_idx + 1][0])):
            gyro_idx += 1
            if (gyro_idx < gyro_len):
                continue
            else:
                break

    if(accel[i][0] < ori[ori_idx][0] and ori_idx == 0):
        pass 
    elif(ori_idx == ori_len):
        pass 
    else:
        while(not (ori[ori_idx][0] <= accel[i][0] and accel[i][0] < ori[ori_idx + 1][0])):
            ori_idx += 1
            if (ori_idx < ori_len):
                continue
            else:
                break

    output.append((accel[i][0], accel[i][1], accel[i][2], accel[i][3], gyro[gyro_idx][1], gyro[gyro_idx][2], gyro[gyro_idx][3], ori[ori_idx][1], ori[ori_idx][2], ori[ori_idx][3], ori[ori_idx][4]))

name = ['timestamp', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'ori_scalar', 'ori_x', 'ori_y', 'ori_z']

output_file_path = row_data_path.split('.')[0] + '_.csv'
df = pd.DataFrame(data = output, columns = name)
df.to_csv(output_file_path)

