from django.http import HttpResponse

import pandas

import preprocess as pre 
from dtw import DTW
from dtw import cosine_cost
from vector import Vector
import json

accel_data = []

def index(request):
    label = 'Not Start'
    global accel_data
    dtw = DTW()
    dtw.tamplate_load('model.npy')
    threshold = 20
    if (request.method == 'POST'):
        received_json_data = json.loads(request.body)
        accel_data.append(Vector((received_json_data['accel_x'], received_json_data['accel_y'], received_json_data['accel_z'])))
        if (len(accel_data) == 150):
            #amplitudes = list(map(lambda v: v.modulus(), accel_data))
            #print(amplitudes)
            #if (max(amplitudes) - min(amplitudes) >= threshold):
            label = dtw.test(accel_data, cosine_cost)  
            accel_data = []  
        return HttpResponse(label)
    else:
        '''
        motion_period = 5 # 5s
        frequency = 50 # 50Hz
        period = motion_period * frequency

        gesture_dataflow_path = 'simulation.csv'
        gestures = pre.data_segmentation(gesture_dataflow_path, period, 2, 5)

        for i in range(0, len(gestures)):
            label = dtw.test(gestures[i], cosine_cost) 
        '''
        return HttpResponse('Wrong POST')
    