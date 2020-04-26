import math 

class Vector:
    '''
        vector class in this project
    '''
    def __init__(self, value):
        '''
            value is a tuple
        '''
        self.value = value 

    def __str__(self):
        return '{}'.format(self.value)

    def __add__(self, other):
        return Vector(tuple(i+j for i, j in zip(self.value, other.value))) 

    def __sub__(self, other):
        return Vector(tuple(i-j for i, j in zip(self.value, other.value))) 

    def __neg__(self):
        return Vector(tuple(map(lambda x: -x, self.value)))

    def __mul__(self, scalar):
        return Vector(tuple(map(lambda x: x*scalar, self.value)))

    def dot(self, other):
        return sum(i * j for i, j in zip(self.value, other.value))

    def modulus(self):
        return math.sqrt(sum(i*i for i in self.value))
     

def cross_product(vector_1, vector_2):
    '''
        To compute the cross product of two 3-D vectors 
        Returns the result vector in the form of tuple 
        This function only works over 3-D vectors, so we 
        inplement it outside the class 
    '''
    if (len(vector_1) != 3 or len(vector_2) != 3):
        raise RuntimeError('vector length is not 3')

    return (vector_1[1]*vector_2[2] - vector_1[2]*vector_2[1], \
            vector_1[2]*vector_2[0] - vector_1[0]*vector_2[2], \
            vector_1[0]*vector_2[1] - vector_1[1]*vector_2[0])

