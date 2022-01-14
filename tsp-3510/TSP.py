import sys
import time
zero = time.time()
import math
import random
import numpy as np
import pandas as pd

def start(totalPopulation, order):
    specificPopulation = []
    specificPopulation.append(list(order))
    individualCity = 0
    stop = totalPopulation - 1
    #Create List of cities
    while individualCity < (stop):
        random.shuffle(order)
        specificPopulation.append(list(order))
        individualCity += 1
    return specificPopulation

def totalOrder(nextCity):
    answer = 0
    cityCount = 0
    stop = len(nextCity) - 1
    while cityCount < stop:
        td = totalDistance[nextCity[cityCount]][nextCity[cityCount + 1]]
        answer += td
        cityCount += 1
    answer += totalDistance[nextCity[-1]][nextCity[0]]
    return 1 / answer

def distance(cityA, cityB):
	xdis = abs(cityA[1] - cityB[1])
	ydis = abs(cityA[2] - cityB[2])
	distance = math.sqrt((xdis**2) + (ydis**2))
	return distance

def slice(first, second):
    num = random.randint(0,len(first)-1)
    three = first[0:num]
    count = 0
    stop = len(second)
    while count < stop:
        if second[count] not in three:
            three.append(second[count])
        count += 1

    
    return three


def select(newOrder, outside):
    #Make list of parent routes
    val_best = 0
    count = 0
    while count < outside:
        ind = random.randint(0,len(newOrder)-1)
        if newOrder[ind] > val_best:
            best = ind
            val_best=newOrder[best]
        count += 1
        return best



def switch(amount, alpha, beta):
    one = amount.pop(alpha)
    two = amount.pop(beta - 1)
    amount.insert(alpha, two)
    amount.insert(beta, one)
    return amount

def TSP(size, length, mutation, pool, actualSize, cieling):
    fit = []
    order = []
    random.seed(15)
    counter = 0
    while counter < length:
    	order.append(counter)
    	counter += 1
    population = start(size, order)
    newOrder = [totalOrder(nextPop) for nextPop in population]
    while (time.time() - zero <= cieling):
        #Program will terminate at the end of time limit as specified in arguements
        try:
            print("Processing...")
            newCity = []
            poolsize = int(pool*size)
            newCityLength = len(newCity)
            while(len(newCity) < poolsize):
                    first = population[select(newOrder, actualSize)]
                    second = population[select(newOrder, actualSize)]
                    thirdAddition = slice(first,second)
                    newCity.append(thirdAddition)
            poolMutation = int((pool + mutation) * size)
            while(len(newCity) < poolMutation):
                above = population[select(newOrder, actualSize)]
                randomX=  random.randint(0, length - 1)
                randomY = randomX
                while(randomY != randomX):
                    randomY = random.randint(0, length - 1)
                newCity.append(switch(above, randomX, randomY))
            answerPlease = sorted(newOrder)
            while(len(newCity) < size):
                newCity.append(population[newOrder.index(answerPlease.pop())])
            newOrder =[totalOrder(newCityAnswer) for newCityAnswer in newCity]
            mostFit = max(newOrder)
            fit.append(mostFit)
            population = newCity
        except IndexError:
            print("Index out of bounds")

    return (newCity[newOrder.index(mostFit)],fit)

cities = pd.read_csv(sys.argv[1],sep=" ",header=None)
cieling = int(sys.argv[3])

totalDistance = []
cityCount = 0
stop = len(cities)
for i in range(len(cities)):
    current = []
    for j in range(len(cities)):
        current.append(distance(cities.iloc[i,:],cities.iloc[j,:]))
    totalDistance.append(current)
length = len(cities)
actualSize = 2
size = 100 * (length + 1)
pool = 0.5
mutation = 0.1
final, fit = TSP(size, length, mutation, pool, actualSize, cieling)
negative = 1 / totalOrder(final)
writeSystem = open(sys.argv[2],"w+")
writeSystem.write("Average: %d\r\n" % negative)
writeSystem.write("Tour: ")
for i in range(len(final)):
    #Actual writing, every visited node is printed here
	writeSystem.write("%d " % final[i])
writeSystem.write("%d " % final[0])
writeSystem.close()



def main():
    print("Done, please check the mat-output.txt file for results :)")


if __name__ == "__main__":
    main()