import numpy as np 

def predict(X, Theta):
    return X @ Theta

def computerCost(X, y, Theta):
    predicted = predict(X, Theta)
    #fuction computerCost
    sqr_error = (predicted - y) ** 2
    sum_error = np.sum(sqr_error)
    m = np.size(y)
    J = (1/(2*m))*sum_error
    return J

def computerCost_Vec(X, y, Theta):
    error = predict(X, Theta) - y
    m = np.size(y)
    J = (1/(2 * m))*np.transpose(error) @ error
    return J

def printProgressBar (iteration, total, suffix = ''):
    percent = ("{0:." + str(1) + "f}").format(100 * ((iteration+1) / float(total)))
    filledLength = int(50 * iteration // total)
    bar = '=' * filledLength + '-' * (50- filledLength)
    print('\rTraining: |%s| %s%%' % (bar, percent), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def GradientDescent(X, y, alpha = 0.001, iter = 5000):
    # Đặt giá trị ban đầu của theta = 0 
    theta = np.zeros(np.size(X,1))
    # lưu giá trị J trong quá trình lặp
    J_hist = np.zeros((iter, 2))
    # ma trận nghịch đảo
    X_T = np.transpose(X)
    # kích thước của trainning set 
    m = np.size(y)
    # biến ktra GD
    pre_cost = computerCost(X, y, theta)
    for i in range(0, iter):
        printProgressBar(i,iter)
        # tính sai số
        error = predict(X, theta) - y
        theta = theta - (alpha/m)*(X_T @ error)
        cost = computerCost(X, y, theta)
        if np.round(cost, 15) == np.round(pre_cost, 15):
            # In ra vòng lặp hiện tại
            print('Reach optima I = %d; J = %.6f'%(i,cost))
            # thêm các index còn lại sau khi breack
            J_hist[i:,0] = range(i,iter)
            # Giá trị J sau khi breack sẽ về như cũ 
            J_hist[i:,1] = cost
            break
        # Update precost
        pre_cost = cost
        # lưu lại index vòng lặp hiện tại
        J_hist[i,0] = i
        # lưu lại J hiện tại
        J_hist[i,1] = cost
    yield theta
    yield J_hist

