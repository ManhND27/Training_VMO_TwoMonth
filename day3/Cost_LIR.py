import numpy as np 
from function import*

raw = np.loadtxt("dataLR.txt", delimiter = ',')
np.size(raw,1)

y = raw[:, 2]
X = np.zeros((np.size(y), np.size(raw,1)))
X[:, 0] = 1
X[:, 1:] = raw[:,0:2]
theta = np.array([1,2,3])

print(computerCost(X, y, theta), computerCost_Vec(X, y, theta))