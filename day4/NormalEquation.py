import numpy as np
from function import *

[X, y] = Loadtxt("data.txt")
Theta = NormEqn(X, y)
inp = np.array([1, 1650, 3])
predict = predict(inp, Theta)
print(predict, inp)