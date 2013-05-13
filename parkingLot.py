##########################################################################################
#
# This program was created to demonstrate what to do when arriving to a full
# parking lot with no extra parking space. There are 2 options that you can do,
# either to sit idle and wait until someone will leave, or to drive around impatiently
# like a madman, waiting for someone to leave.
# This program uses the monte carlo method to simulate an approximation of the time 
# bieng wasted by either driver and plots them on a graph.
# I have made sevral hypotheses:  
#  * a car looking for parking can only have control over 8 cars from either direction
#  * if the car isn't within the distance that it controls (8 cars) - the freed parking 
#    space will be taken by another driver.
#  * the parking lot is only one lane long with parking on either side.
#  * a car driving in the parking lot is driving at 5MPH.
#  * the size of every car is 10 ft. by 7 ft.
#  * every 30 seconds a new parked car will leave the parking lot (undependent of the time
#    being there).
#    NOTE: we can add weights to newly parked cars, in order to get a better assumption
# The parking lot is structured as a cartesian plane, with the cars driving
# up the y axis where x = 0, and the parked cars are located at x-1 and x+1.
# with each car taking up the width of 7 ft.
# For example, the first parked car on the left side will be at location (-1,0)
# to(-1,6), the second car will be at location (-1,7) - (-1,13) etc. and the
# same will be at the right side with the first car at location (1,0) - (1,6) etc.
# NOTE: most assumptions that I made are (highly) debatable, so take it with a grain of salt!
#
# created by Chaim Pollak cschaimp@gmail.com 
###########################################################################################
import random
import pylab



class Parking_Lot(object):
    
    def __init__(self, size = 1000):
        self.parking_spot = []
        self.size = size
        
    def addCar(self, car):
        if car in self.parking_spot:
            raise ValueError('Duplicate car in same spot')
        self.parking_spot.append(car)
            
    def removeCar(self, car):
        if not car in self.parking_spot:
            raise ValueError('car not in parking lot')
        self.parking_spot.remove(car)
    
    def fillUp(self):
        i = 0
        while i < self.size:
            leftNewCar = Car(-1, i)
            self.addCar(leftNewCar)
            rightNewCar = Car(1, i)
            self.addCar(rightNewCar)
            i += 7
            
    def getLotSize(self):
        return self.size

    def getAmountCars(self):
        return len(self.parking_spot) -1 #len() counts from 0

    def getCars(self):
        return self.parking_spot #NOTE: this returns the actual list, not a clone

            
            
            

class Car(object):
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getLoc(self):
        return (self.x, self.y)

    def changeLoc(self, x, y):
        self.x = x
        self.y = y

    def distFrom(self, other):
        ox = other.getX()
        oy = other.getY()
        if abs(ox - self.x) != 1:
            raise ValueError('car in wrong lane')
        yDist1 = abs(self.y - oy)
        yDist2 = abs((self.y + 10) - oy) #there is a front and a back to a car
        return min(yDist1, yDist2)
    
    def __str__(self):
        return 'This car is located at ' + '<' + str(self.x) + ', ' + str(self.y) + '>'

    

    
    
class EasyDriver(Car):
    def __init__(self, parkingLotSize):
        self.x = 0
        self.y = random.choice(range(parkingLotSize))
        
        
       

class ImpatientDriver(Car):
    def __init__(self, parkingLotSize, MPH = 5):
        self.feetPS =  MPH * 5280/ 3600 # computing MPH to feet per second (round to int)
        self.parkingLotSize = parkingLotSize
        self.x = 0
        self.y = 0
           
    def updateLocation(self, seconds_passed):
        self.y = ((seconds_passed * self.feetPS) + self.y) % self.parkingLotSize
        
   
## this function is intended to simulate the Impatient driver (with the amount of space
## set to 56 - for 8 cars (8*7)

def simImpatientDriver(amound_of_space = 56):
    Parking = Parking_Lot(1000)
    Parking.fillUp()
    driver = ImpatientDriver(Parking.getLotSize())
    Parking.addCar(driver)
    parked_cars = Parking.getCars()
    time_lost = 0
    parking_found = False
    
    while not parking_found:
        leaving_car = random.choice(parked_cars)
        while leaving_car == driver:
            leaving_car = random.choice(parked_cars)
        driver.updateLocation(30)
        time_lost += 30
        if driver.distFrom(leaving_car) < amound_of_space:
            parking_found = True
            return time_lost

## this function is intended to simulate the easy driver (with the amount of space
## set to 56 - for 8 cars (8*7)

def simEasyDriver(amound_of_space = 56):
    Parking = Parking_Lot(1000)
    Parking.fillUp()
    driver = EasyDriver(Parking.getLotSize())
    Parking.addCar(driver)
    parked_cars = Parking.getCars()
    time_lost = 0
    parking_found = False
    
    while not parking_found:
        leaving_car = random.choice(parked_cars)
        while leaving_car == driver:
            leaving_car = random.choice(parked_cars)
        time_lost += 30
        if driver.distFrom(leaving_car) < amound_of_space:
            parking_found = True
            return time_lost

        
## this function is intended to actually run the simulation of both drivers and plot
## them on a graph - to get a visual sense of the time.(using enthought (EPD) for pylab)

def parkingtest(numTrials = 25):
    meanImpatientTiming = []
    meanEasyTiming = []
    for i in range(numTrials):
        averageImpatientTiming = []
        averageEasyTiming = []
        for i in range(10000):
            averageImpatientTiming.append(simImpatientDriver())
            averageEasyTiming.append(simEasyDriver())
        meanImpatientTiming.append(sum(averageImpatientTiming)/len(averageImpatientTiming))
        meanEasyTiming.append(sum(averageEasyTiming)/len(averageEasyTiming))
    pylab.plot(meanEasyTiming, 'b-',
               label = 'easy driver')
    pylab.plot(meanImpatientTiming, 'g-.',
               label = 'impatient driver')
    pylab.title('time to find a parking spot (mean of 10000 trials)')
    pylab.xlabel('amount of times trials ran')
    pylab.ylabel('time taken in seconds')
    pylab.legend()
    pylab.show()


## let the fun begin! 
parkingtest()

