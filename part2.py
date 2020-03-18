##########################################################################
# Imports
##########################################################################
import csv
import sys
import random
import numpy as np

##########################################################################
# Basic
##########################################################################

def EM(numClusters):
    print("Starting EM")
    #based on the video we had to watch for class:
    #https://www.youtube.com/watch?v=QQJHsKfNqG8&list=PLAwxTw4SYaPmaHhu-Lz3mhLSj-YH-JnG7&index=53
    points = []

    #read from csv
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            points.append(list(np.float_(row)))
    
    #choose random starting centers from the list of points
    centers = np.empty(numClusters, dtype=object)
    tempPoints = points.copy()
    random.shuffle(tempPoints)
    for i in range(numClusters):
        centers[i] = tempPoints.pop()
    clusterGuess = np.empty(len(points), dtype=object)

    #Perform EM
    #currently doing 10 iterations could be more
    '''todo: add random restarts'''
    for count in range(10):
        
        #get the current variances now so I don't have to do that later
        #for performance reasons (I think)
        variances = centers.copy()
        for centerIndex in range(len(centers)):
            variances[centerIndex] = variance(points, centers[centerIndex])

        #expecatation
        for counter in range(len(points)):
            point = points[counter]
            bestGuess = (0, expectation(points, centers, point, centers[0], variances[0]))
            for centerIndex in range(len(centers)):
                testCenter = expectation(points, centers, point, centers[centerIndex], variances[centerIndex]) 
                if testCenter > bestGuess[1]:
                    bestGuess = (centerIndex, testCenter)
            clusterGuess[counter] = bestGuess
        
        #maximization
        for count in range(len(centers)):
            tempPoints = []
            for index in range(len(clusterGuess)):
                if clusterGuess[index][0] == count and clusterGuess[index][1] >= 0.6:
                    tempPoints.append(points[index])
            centers[count] = maximization(tempPoints, centers, centers[count], variances[count])
    
    #print the calculated centerss
    print(centers)



#does the probability calculation
def probablity(x, mu, variance):
    sigma = variance
    if distance(x, mu) == 0:
        return np.exp(-0.5 * np.log(np.power(sigma, 2)) * np.log((np.power((10**-10), 2))))
    else:
        return np.exp(-0.5 * np.log(np.power(sigma, 2)) * np.log((np.power((distance(x, mu)), 2))))

#calculates the variance
def variance(points, mu):
    s2 = 0
    for x in points:
        s2 += np.power((distance(x, mu)), 2)
    return s2 / (len(points))

#calculates a point minus another point
def distance(p1, p2):
    dist = 0
    for index in range(len(p1)):
        dist += np.power((p1[index]-p2[index]), 2)
    dist = np.sqrt(dist)
    return dist

# calculates the expectation
# points are the x values
# centers is the different means
# i and j are point and the center
def expectation(points, centers, i, j, variance):
    v = variance
    p = probablity(i, j, v)
    total = 0.0
    for x in centers:
        total += probablity(i, x, v)
    return p/total

# does the maximization
def maximization(points, centers, j, variance):
    sum = np.zeros(len(points[0]))
    denom = 0
    for x in points:
        for count in range(len(sum)):
            sum[count] += expectation(points, centers, x, j, variance) * x[count]
        denom += expectation(points, centers, x, j, variance)
    average = points[0].copy()
    for count in range(len(average)):
        average[count] = sum[count]/denom
    return average

##########################################################################
# Calculate the number of points (BIC)
##########################################################################
def BIC():
    print("Starting BIC...")
    #do BIC
    numClusters = 0

    print("Completed BIC there are " + str(numClusters) + " clusters!")
    EM(numClusters)

##########################################################################
# Main method and command line stuff
##########################################################################
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("The program needs 2 arguments file and number of clusters")
        print("Example input: python part2.py test.csv 3")
    elif sys.argv[2] == "0":
        BIC()
    else:
        EM(int(sys.argv[2]))