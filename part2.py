##########################################################################
# Imports
##########################################################################
import csv
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import time

#########################################################################
# Basic EM Stuff
#########################################################################

def EM(numClusters, points):
    print("Running EM")
    #based on the video we had to watch for class:
    #https://www.youtube.com/watch?v=QQJHsKfNqG8&list=PLAwxTw4SYaPmaHhu-Lz3mhLSj-YH-JnG7&index=53
    

    #Perform EM
    bestLL = 0
    bestCenters = []
    #currently doing 10 iterations should be more
    startTime = time.time()
    curTime = startTime
    while(curTime < startTime + 10):
        centers, clusterGuess, LL = EMIteration(points, numClusters)

        if LL > bestLL:
            bestLL = LL
            bestCenters = centers

        curTime = time.time()
        
    #print the calculated centerss
    print("Time elapsed: " + str(curTime-startTime) + " seconds")
    print("The centers are: " + str(centers))
    print("The log likelihood is: " + str(LL))

    plotPoints = points.copy()
    plot(plotPoints, centers)

    


#Does one iteration of EM
def EMIteration(points, numClusters):
    #choose random starting centers from the list of points
    centers = np.empty(numClusters, dtype=object)
    tempPoints = points.copy()
    
    random.shuffle(tempPoints)
    for i in range(numClusters):
        centers[i] = tempPoints.pop()
    clusterGuess = np.empty(len(points), dtype=object)
    for index in range(len(clusterGuess)):
        clusterGuess[index] = (0,0)

    for count in range(10):

        #get the current variances
        variances = centers.copy()
        for centerIndex in range(len(centers)):
            variances[centerIndex] = variance(points, centers[centerIndex])

        #expecatation
        for counter in range(len(points)):
            if clusterGuess[counter][1] < 0.999:
                point = points[counter]
                bestGuess = (0, 0)
                total = 0.0
                for cIndex in range(len(centers)):
                    total += probablity(point, centers[cIndex], variances[cIndex])
                for centerIndex in range(len(centers)):
                    testCenter = expectation(points, centers, point, centers[centerIndex], variances[centerIndex], total) 
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

        logLikelihood = calculateLogLikelihood(points, centers, variances)


    #get the logLikelihood
    variances = centers.copy()
    for centerIndex in range(len(centers)):
        variances[centerIndex] = variance(points, centers[centerIndex])
    logLikelihood = calculateLogLikelihood(points, centers, variances)

    return centers, clusterGuess, logLikelihood


#does the probability calculation
def probablity(x, mu, sigma):
    d = distance(x, mu)
    if d == 0:
        return np.exp(-0.5 * np.log(np.power(sigma, 2)) * np.log((np.power((10**-10), 2))))
    else:
        return np.exp(-0.5 * np.log(np.power(sigma, 2)) * np.log(d))

#calculates the variance
def variance(points, mu):
    s2 = 0
    for x in points:
        s2 += distance(x, mu)
    return s2 / (len(points))

#calculates a point minus another point
def distance(p1, p2):
    dist = 0
    for index in range(len(p1)):
        dist += np.power((p1[index]-p2[index]), 2)
    return dist

# calculates the expectation
# points are the x values
# centers is the different means
# i and j are point and the center
def expectation(points, centers, i, j, v, total):
    p = probablity(i, j, v)
    return p/total

# does the maximization
def maximization(points, centers, j, variance):
    sum = np.zeros(len(points[0]))
    denom = 0
    for x in points:
        total = 0.0
        for c in centers:
            total += probablity(x, c, variance)
        for count in range(len(sum)):
            sum[count] += expectation(points, centers, x, j, variance, total) * x[count]
        denom += expectation(points, centers, x, j, variance, total)
    average = points[0].copy()
    for count in range(len(average)):
        average[count] = sum[count]/denom
    return average


#open points
def readCSVPoints():
    points = []

    #read from csv
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            points.append(list(np.float_(row)))

    return points

#calculates the log likelihood
#based on the spreadsheet candy example
# LL = sum LL of each point
# LL of each point = data * Log(P(data))
### I'm not sure what the data means but I used the expectation as the data?
def calculateLogLikelihood(points, centers, v):
    LL = 0
    total = 0
    for point in points:
        for cIndex in range(len(centers)):
            total += probablity(point, centers[cIndex], v[cIndex])
        for c in range(len(centers)):
            LL += expectation(points, centers, point, centers[c], v[c], total) * probablity(point, centers[c], v[c])
    return LL

#########################################################################
# Calculate the number of points (BIC)
#########################################################################

#https://en.wikipedia.org/wiki/Bayesian_information_criterion#Definition
def BIC(points):
    print("Starting BIC...")
    #do BIC
    numClusters = 1
    bestBIC = float('-inf')

    k=1
    n = len(points)

    x = n
    if x > 10:
        x = 10
    
    for i in range(1, x):
        L = EMIteration(points, numClusters)[2]
        temp = calculateBIC(L, n, k)
        if temp >= bestBIC:
            numClusters = i
            bestBIC = temp
        

    print("Completed BIC there are " + str(numClusters) + " clusters!")
    print("The BIC score is: " + str(bestBIC))
    EM(numClusters, points)

#calculates BIC value as mentioned in the wikipedia article
def calculateBIC(L, n, k=1):
    b = (np.log(n) * k) - (2 * np.log(L))
    return b


#########################################################################
# scatter plots the points and cluster centers
#########################################################################
def plot(points, centers):
    x = []
    y = []
    for i in points:
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x, y)

    fig = plt.gcf()
    ax = fig.gca()
    for i in centers:
        center_circle = plt.Circle((i[0], i[1]), 0.01, color = 'g')
        # TODO radius of circle hard-coded, probably a better way to calculate
        cluster_circle = plt.Circle((i[0], i[1]), 1, fill=False, edgecolor=random.choice(['r','b','y']))
        ax.add_artist(center_circle)
        ax.add_artist(cluster_circle)

    plt.show()

#########################################################################
# Main method and command line stuff
#########################################################################
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("The program needs 2 arguments file and number of clusters")
        print("Example input: python part2.py test.csv 3")
    elif sys.argv[2] == "0":
        points = readCSVPoints()
        BIC(points)
    else:
        points = readCSVPoints()
        EM(int(sys.argv[2]), points)
