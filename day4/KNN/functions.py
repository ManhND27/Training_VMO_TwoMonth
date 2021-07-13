import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.lib import math
from numpy.lib.function_base import delete
import pandas as pd
from numpy import dtype, genfromtxt

def loadData(path):
    data = np.loadtxt(path, delimiter = ',', dtype=str)
    data = np.array(list(data))
    #data = np.delete(data, 0, 0)
    data = np.delete(data, 0, 1)
    np.random.shuffle(data)
    trainSet = data[:100]
    testSet = data[100:]
    yield trainSet
    yield testSet

def calcDistancs(pointA, pointB, numOfFeature = 4):
    tmp = 0
    for i in range(numOfFeature):
        tmp += (float(pointA[i]) + float(pointB[i])) ** 2
    return math.sqrt(tmp)

def kNearestNeighbor(trainSet, point, k):
    distances = []
    for item in trainSet:
        distances.append({
            "label": item[-1],
            "value": calcDistancs(item, point)
        })
    distances.sort(key=lambda x: x["value"])
    labels = [item["label"] for item in distances]
    return labels[:k]

def findMostOccur(arr):
    labels = set(arr) # set label
    ans = ""
    maxOccur = 0
    for label in labels:
        num = arr.count(label)
        if num > maxOccur:
            maxOccur = num
            ans = label
    return ans

