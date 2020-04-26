# the following code is used to locate the bug in quaternion_rotation
'''
import math 

def scalar_product(k, vector):

    return tuple(map(lambda x: x*k, vector))

def dot_product(vector_1, vector_2):
  
    return sum(i * j for i, j in zip(vector_1, vector_2))  
     
def cross_product(vector_1, vector_2):

    return (vector_1[1]*vector_2[2] - vector_1[2]*vector_2[1], \
            vector_1[2]*vector_2[0] - vector_1[0]*vector_2[2], \
            vector_1[0]*vector_2[1] - vector_1[1]*vector_2[0])

def vector_plus(vector_1, vector_2):
  
    return tuple(i+j for i, j in zip(vector_1, vector_2))


def quaternion_rotation(q, v):
    cos_alpha_2 = q[0]
    sin_aplha_2 = math.sqrt(1 - cos_alpha_2 ** 2)
    u = (q[1] / sin_aplha_2, q[2] / sin_aplha_2, q[3] / sin_aplha_2)
    
    cos_alpha = 2 * cos_alpha_2 ** 2 - 1
    sin_alpha = 2 * sin_aplha_2 * cos_alpha_2 

    # to compute the components of v parallel to u
    v_parallel_coefficient = dot_product(v, u) / dot_product(u, u)
    
    v_parallel = scalar_product(v_parallel_coefficient, u) 
    
    # to compute the components of v perpendicular to u 
    v_perpendicular = vector_plus(v, (-v_parallel[0], -v_parallel[1], -v_parallel[2]))

    # the final result 
    term1 = scalar_product(cos_alpha, v_perpendicular)
    term2 = scalar_product(sin_alpha, cross_product(u, v))

    intermedia = vector_plus(term1, term2)
    result = vector_plus(intermedia, v_parallel)
    return result

q = (-0.02987, 0.38079, 0.91837, 0.10358)
v = (8.60622, -4.68799, -0.22147)

print(quaternion_rotation(q, v))
'''

'''
import csv 
accel = []
gyro = []
sensor_data_file_path = 'data/sync.csv'

with open(sensor_data_file_path) as sensor_data_file:
    sensor_data_file_csv = csv.reader(sensor_data_file)
    for line in sensor_data_file_csv:
        if (line[0] == '1'):
            accel.append((float(line[1]), float(line[2]), float(line[3]), float(line[4])))
        else:
            gyro.append((float(line[1]), float(line[2]), float(line[3]), float(line[4])))


print(len(accel))
print(len(gyro))
'''


import pandas as pd 
import csv 
import matplotlib.pyplot as plt
import math 

# df = pd.read_csv('data/wave_down/wave_down_5_.csv')
#df = pd.read_csv('simulation.csv')
df = pd.read_csv('test_data/test_2_.csv')

acceleration = list(zip(df['accel_x'].values.tolist(), df['accel_y'].values.tolist(), df['accel_z'].values.tolist()))
angular_velocities = list(zip(df['gyro_x'].values.tolist(), df['gyro_y'].values.tolist(), df['gyro_z'].values.tolist()))
orientations = list(zip(df['ori_scalar'].values.tolist(), df['ori_x'].values.tolist(), df['ori_y'].values.tolist(), df['ori_z'].values.tolist()))

accel = list(map(lambda a : math.sqrt(a[0]**2 + a[1]**2 + a[2]**2) , acceleration))

x_axis = list(range(len(accel)))

plt.plot(x_axis, accel)
plt.show()




'''
import numpy as np

class sequence_template:
    def __init__(self, sequence, mu, sigma, k, label):
        self.sequence = sequence
        self.mu = mu
        self.sigma = sigma
        self.k = k
        self.label = label

a = sequence_template([1,2,3,4,5], 3, 2, 2, '123')
b = sequence_template([1,2,3,4,5], 3, 2, 2, '123')

c = [a,b]

d = np.array(c)

np.save("filename.npy",d)

e = np.load("filename.npy", allow_pickle=True)
print(e[0].sequence)
'''
'''
import os 
path = 'data'
data_dir = os.listdir(path)
for d in data_dir:
    print(os.listdir(path + '/' + d))

print(data_dir)
'''



