import numpy as np 
import matplotlib.pyplot as plt
from function import * 

[X, y] = Loadtxt('data.txt')
[X, mu, s] = Normalize(X)
[Theta, J_hist] = GradientDescent(X,y,0.1,400)
input = np.array([1,1650,3])
input = (input-mu)/s
input[0] = 1
predict = predict(input,Theta)
print('%.2f'%(predict))