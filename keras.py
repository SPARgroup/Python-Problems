import keras
import math
import numpy

def sigmoid(x):
    return (1/(1+math.exp(-1 * x /200)))

# print(sigmoid(1))
# print(sigmoid(0))
# print(sigmoid(23))
# print(sigmoid(22))
# print(sigmoid(21))
# print(sigmoid(20))

print(sigmoid(2))
print(sigmoid(3))