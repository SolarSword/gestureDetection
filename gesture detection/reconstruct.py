'''
    To compute the continuous sum of the data flow from accelerometer.
    I made an assumption here that the initial speed and accelerometer are 0.
    By using quaternion to revert the accelerometer to a fixed coordination system,
    we can compute the velocity of the Fitbit sensors. Then the displacement of the sensors 
    can be collected by computing the continuous sum of the velocity flow.

    That is how this program works theoretically. 
'''
import math 
import csv 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from copy import deepcopy 
import pandas as pd 

def scalar_product(k, vector):
    '''
        To compute the scalar product between a scalar and a vector 
    '''
    return tuple(map(lambda x: x*k, vector))

def dot_product(vector_1, vector_2):
    '''
        To compute the dot product of two vectors
    '''
    return sum(i * j for i, j in zip(vector_1, vector_2)) 
     
def cross_product(vector_1, vector_2):
    '''
        To compute the cross product of two 3-D vectors 
        Returns the result vector in the form of tuple 
    '''
    return (vector_1[1]*vector_2[2] - vector_1[2]*vector_2[1], \
            vector_1[2]*vector_2[0] - vector_1[0]*vector_2[2], \
            vector_1[0]*vector_2[1] - vector_1[1]*vector_2[0])

def vector_plus(vector_1, vector_2):
    '''
        To compute the plus result between two vectors
    '''
    return tuple(i+j for i, j in zip(vector_1, vector_2))

def vector_negation(vector):
    return tuple(map(lambda x: -x, vector))

def quaternion_rotation(q, v):
    '''
        To compute the rotation result of qvq-1
        input:
            q: q is the rotation quaternion 
            v: v is the pure quaternion to be rotated
        output:
            the result v' in the form of tuple
    '''
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

def balance_gravity(acc, g):
    '''
        input: 
            acc: a 3-D acceleration tuple
            g: local gravity
        output: 
            acceleration after balancing gravity 
    '''
    return (acc[0], acc[1], acc[2] - g)

def suppression_vector(vector, threshold):
    '''
        input:
            vector: the vector to be suppressed
            threshold: suppression threshold 
    '''
    return tuple(map(lambda x: x if x >= threshold else 0, vector))




# sensor_data_file_path = 'olddata/full_deletion.csv'
sensor_data_file_path = 'data/clockwise_circle/clockwise_circle_1_.csv'

frequency = 1/50

df = pd.read_csv(sensor_data_file_path)

accelerations = list(zip(df['accel_x'].values.tolist(), df['accel_y'].values.tolist(), df['accel_z'].values.tolist()))
angular_velocities = list(zip(df['gyro_x'].values.tolist(), df['gyro_y'].values.tolist(), df['gyro_z'].values.tolist()))
orientations = list(zip(df['ori_scalar'].values.tolist(), df['ori_x'].values.tolist(), df['ori_y'].values.tolist(), df['ori_z'].values.tolist()))

nms_accelerations = deepcopy(accelerations)
nms_angular_velocities = deepcopy(angular_velocities)

accel_length = len(accelerations)
for i in range(0, accel_length):
    if (i == 0):
        continue 

    if (nms_accelerations[i][0] - nms_accelerations[i-1][0] < 0.5):
        nms_accelerations[i] = (0, nms_accelerations[i][1], nms_accelerations[i][2])

    if (nms_accelerations[i][1] - nms_accelerations[i-1][1] < 0.5):
        nms_accelerations[i] = (nms_accelerations[i][0], 0, nms_accelerations[i][2])

    if (nms_accelerations[i][2] - nms_accelerations[i-1][2] < 0.5):
        nms_accelerations[i] = (nms_accelerations[i][0], nms_accelerations[i][1], 0)

#timestamps = [] 
#accelerations = []
#angular_velocities = []
#orientations = [] 

# data form is like this
# timestamp, x_accel, y_accel, z_accel, x_ang, y_ang, z_ang, ori_a, ori_x, ori_y, ori_z  


# this part used to read the old data 
'''
with open(sensor_data_file_path) as sensor_data_file:
    sensor_data_file_csv = csv.reader(sensor_data_file)
    for line in sensor_data_file_csv:
        timestamps.append(line[0])
        accelerations.append((float(line[1]), float(line[2]), float(line[3])))
        angular_velocities.append((float(line[4]), float(line[5]), float(line[6])))
        orientations.append((float(line[7]), float(line[8]), float(line[9]), float(line[10])))

        #accelerations.append((float(line[0]), float(line[1]), float(line[2])))
'''


# try to compute the continous sum of the accelerations 
length = len(accelerations) # all lengths of the 4 lists are the same  
velocities = [0] * length
displacements = [0] * length # relative to the initial place of the sensors 


for i in range(length):
    # R(p) = qpq-1 (Quaternions rotation transformation) 

    # According to Wiki https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
    
    acc_rotate = quaternion_rotation((orientations[i][0], -orientations[i][1], -orientations[i][2], -orientations[i][3]), accelerations[i])
    # the gravity in Singapore is around 9.7807
    acc_balance = balance_gravity(acc_rotate, 9.7807)
    acc_balance = suppression_vector(acc_balance, 1.5)
    acc_balance = balance_gravity(accelerations[i], 9.7807)
    if (i == 0):
        velocities[i] = scalar_product(frequency, acc_balance)
        displacements[i] = scalar_product(frequency, velocities[i])
    else:
        velocities[i] = vector_plus(velocities[i-1], scalar_product(frequency, acc_balance))
        displacements[i] = vector_plus(displacements[i - 1], scalar_product(frequency, velocities[i]))



# to draw the reconstruct displacement graph 
x = []
y = []
z = []

for i in range(length):
    x.append(displacements[i][0])
    y.append(displacements[i][1])
    z.append(displacements[i][2])  

ax = plt.subplot(111, projection='3d')
ax.scatter(x, y, z, c='y')

ax.set_zlabel('Z')  
ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()