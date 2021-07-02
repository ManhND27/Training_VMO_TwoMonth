import numpy as np 
import matplotlib.pyplot as plt 
from function import *  


[X, y] = Loadtxt('data.txt')
print(X.shape)
[X, mu, s] = Normalize(X)
[Theta, J_hist] = GradientDescent(X, y)
input = np.array([1,1650,3])
input = (input-mu)/s
#Lưu ý sửa lại x0 = 1
input[0] = 1
predict = predict(input,Theta)
print('%.2f$'%(predict))
