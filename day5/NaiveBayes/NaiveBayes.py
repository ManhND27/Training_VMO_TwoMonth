import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
from pandas.core.construction import sanitize_array

def defindTrainTest(f):
    y = f[:,1] + 1
    m=0
    for i in y:
        #print(i)
        if i == 1:
            m += i
    m = m/len(y)
    #print(m)
    # defind X 
    X = f[:,3:]
    yield y
    yield X

def train(X, y):
    N = X.shape[0]
    D = X.shape[1]
    K = len(np.unique(y))
    theta = np.zeros(K, )
    mu = np.zeros(K, D)
    sigma = np.zeros(K, D)
    for i in range(1, k+1):
        for j in y :
            if j == i:
                theta[i] += j
        theta[i] = theta[i]/len(y)
            
f = np.loadtxt("./data/wdbc.txt", delimiter = ",")
#print(np.shape(f))
#y = A[:,2].+1

X = np.array([[1,2,3,4]])
N = X.shape[0]
D = X.shape[1]
print("{}, {}".format(N,D))
