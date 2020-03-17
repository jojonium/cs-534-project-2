import csv
import sys
import random
import numpy as np

def EM(numClusters):
    #based on the video we had to watch for class:
    #https://www.youtube.com/watch?v=QQJHsKfNqG8&list=PLAwxTw4SYaPmaHhu-Lz3mhLSj-YH-JnG7&index=53
    points = []
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            points.append(list(np.float_(row)))
    centers = np.empty(numClusters, dtype=object)
    tempPoints = points.copy()
    random.shuffle(tempPoints)
    for i in range(numClusters):
        centers[i] = tempPoints.pop()
    clusterGuess = points.copy()
    for count in range(len(points)//2):
        #expecatation
        for counter in range(len(points)):
            point = points[counter]
            bestGuess = centers[0]
            for center in centers:
                testCenter = expectation(points, centers, point, center) 
                if testCenter > expectation(points, centers, point, bestGuess):
                    bestGuess = center
            clusterGuess[counter] = bestGuess
        #maximization
        for count in range(len(centers)):
            centers[count] = maximization(points, centers, centers[count])
    #print the calculated centerss
    print(centers)



#does the probability calculation
def probablity(x, mu, variance):
    sigma = variance
    # print(sigma)
    # print(distance(x,mu))
    # print(-0.5 * np.power(sigma, 2) * (np.power((distance(x, mu)), 2)))
    return np.exp(-0.5 * np.power(sigma, 2) * (np.power((distance(x, mu)), 2)))

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
def expectation(points, centers, i, j):
    v = variance(points, j)
    p = probablity(i, j, v)
    total = 0.0
    for x in centers:
        total += probablity(i, x, v)
    return p/total

# does the maximization
def maximization(points, centers, j):
    sum = np.zeros(len(points[0]))
    denom = 0
    for x in points:
        for count in range(len(sum)):
            sum[count] += expectation(points, centers, x, j) * x[count]
        denom += expectation(points, centers, x, j)
    average = points[0].copy()
    for count in range(len(average)):
        average[count] = sum[count]/denom
    return average


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("The program needs 2 arguments file and number of clusters")
        print("Example input: python part2.py test.csv 3")
    else:
        EM(int(sys.argv[2]))