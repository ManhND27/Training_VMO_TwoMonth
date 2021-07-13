import numpy as np 
from functions import *

trainSet, testSet = loadData("./Iris.txt")
numOfRightAnwser = 0
for item in testSet:
        knn = kNearestNeighbor(trainSet, item, 5)
        answer = findMostOccur(knn)
        numOfRightAnwser += item[-1] == answer
        print("label: {} -> predicted: {}".format(item[-1], answer))
print("Accuracy", numOfRightAnwser/len(testSet))