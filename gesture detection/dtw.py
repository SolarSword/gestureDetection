import csv 
import math 
import numpy as np
import pandas as pd
import random 
from vector import Vector

def cosine_cost(vector_1, vector_2):
    
    return math.acos(round(vector_1.dot(vector_2)/(vector_1.modulus() * vector_2.modulus()), 5))

def euclidean_cost(vector_1, vector_2):
    return (vector_1 - vector_2).modulus()

class sequence_template:
    def __init__(self, sequence, mu, sigma, k, label):
        self.sequence = sequence
        self.mu = mu
        self.sigma = sigma
        self.k = k
        self.label = label

class DTW:
    def __init__(self):
        self.template = []

    def dtw_solver(self, template_, sequence, distance):
        '''
            input:
                template: dtw tamplate
                sequence: a sequence of Vectors waiting to be matching

        '''
        m = len(template_)
        n = len(sequence)
        cumulative_distance = np.zeros((m + 1, n + 1))
        # print(m,' ',n)
        for i in range(1, m + 1):
            cumulative_distance[i,0] = float('inf')

        for i in range(1, n + 1):
            cumulative_distance[0,i] = float('inf')
        #print(cumulative_distance)
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # print(i, ' ', j)
                cumulative_distance[i,j] = distance(template_[i-1], sequence[j-1]) + min(cumulative_distance[i-1,j], cumulative_distance[i-1,j-1], cumulative_distance[i,j-1])
                # print("filling in ({}, {})".format(i,j))

        return cumulative_distance[m, n]

    def dtw_train(self, training_set, training_label, distance_cost):
        '''
            put the sequences with the same label in the same set 
            training time complexity is O(n2)
            input:
                training_set: the training data set 
                training_label: label for this training set
        '''

        total_cost = float('inf')
        iteration_times = len(training_set)
        
        for i in range(0, iteration_times):
            print("iteration %d" %i)
            curr_cost = []
            for j in range(0, iteration_times):
                print("comparing %d" %j)
                curr_cost.append(self.dtw_solver(training_set[i], training_set[j], distance_cost))

            if (sum(curr_cost) < total_cost):
                total_cost = sum(curr_cost)
                template = training_set[i]
                template_cost = curr_cost

        cost_mu = sum(template_cost) / iteration_times
        cost_sigma = math.sqrt(sum(map(lambda x: (x - cost_mu) * (x - cost_mu) , template_cost)) / iteration_times)
        print(cost_mu, cost_sigma)
        print(template_cost)
        # then to train a hyper parameter k to help to compute the result
        # the threshold formula is t = mu + k * sigma
        sensitivity = 0.95 # a parameter to ensure that at least how many percent training set samples are below threshold 
        learning_rate = 0.3
        # according to the 3 sigma principle, most samples will fall within mu ± 3 * sigma
        # so we just initialize the k from -3 to 3 randomly
        under_rate = 0
        k = random.uniform(-3, 3)
        while(True):
            count = 0
            for i in range(0, iteration_times):
                if (template_cost[i] < cost_mu + k * cost_sigma):
                    count += 1
            under_rate = count / iteration_times
            # print(under_rate)
            if (under_rate < sensitivity):
                k = k + learning_rate
            else:
                break
        print(k)
        # training for this group is done 
        self.template.append(sequence_template(template, cost_mu, cost_sigma, k, training_label))
    
    def template_save(self, file_name):
        np_tem = np.array(self.template)
        np.save(file_name, np_tem)
        
    def tamplate_load(self, path):
        self.template = list(np.load(path, allow_pickle=True))

    def test(self, test_sample, distance_cost):
        '''
            feed this function a testing sample and get the result of it
            just use this for accuracy computation. For real scenario use another function 
        ''' 
        if (not self.template):
            raise RuntimeError('No modal avaliable now')
        
        cost_min = float('inf')
        label = 'None'
        for template_ in self.template:
            curr_cost = self.dtw_solver(template_.sequence, test_sample, distance_cost)
            
            if (curr_cost <= template_.mu + template_.k * template_.sigma):
                if (curr_cost < cost_min):
                    cost_min = curr_cost
                    label = template_.label
        
        return label 

