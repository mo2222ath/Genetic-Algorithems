import random


class Chromosome:
    Genes = []
    numberOfTargets = 0
    numberOfTypeWeapons = []
    damagingTarget = []
    threatCoefficient = []
    survivingTarget = []
    numberOfInstanceWeapons = 0
    fitness = 0

    def __init__(self,numberOfTargets,numberOfTypeWeapons,damagingTarget,threatCoefficient):        
        self.numberOfTargets = numberOfTargets
        self.numberOfTypeWeapons = numberOfTypeWeapons
        self.damagingTarget = damagingTarget
        self.threatCoefficient = threatCoefficient
        self.numberOfInstanceWeapons = sum(self.numberOfTypeWeapons)
        self.survivingTarget = self.CalculateSurvivingTarget()
        self.Genes = self.Representation()
        self.fitness = self.Fitness()
        

    def Fitness(self):
        numberOfGenes = len(self.Genes)
        nummberOfWappens = numberOfGenes // self.numberOfTargets
        index = 0
        result = 0
        for i in range(self.numberOfTargets):
            tempInstance = self.numberOfTypeWeapons[:]
            indexOfInstance = 0
            temp = 1
            for j in range(nummberOfWappens):
                if self.Genes[index] == 1 :
                    temp *= self.survivingTarget[indexOfInstance][i]
                index += 1
                if tempInstance[indexOfInstance] > 1 :
                    tempInstance[indexOfInstance] -=1
                else:
                    indexOfInstance +=1
            temp *= self.threatCoefficient[i]
            result += temp
        return result

    def CalculateSurvivingTarget(self):
        SurvivingTarget = []
        for i in range(len(self.damagingTarget)):
            temp = self.damagingTarget[i]
            temp2 = []
            for j in range(len(self.damagingTarget[0])):
                temp2.append(1.0 - temp[j])
            SurvivingTarget.append(temp2)
        return SurvivingTarget

    def Representation(self):
        result = []
        temp = []
        for i in range(self.numberOfTargets):
            for j in range(self.numberOfInstanceWeapons):
                if i==0:
                    n = random.randint(0,1)
                    temp.append(n)
                else:
                    if temp[j] == 0:
                        n = random.randint(0,1)
                        temp[j] = n
            result += temp
            # print("before" , temp)
            for i in range(len(temp)):
                if temp[i] == 1: temp[i] = 2
            # print("After" , temp)
            # print(result)
        for i in range(len(result)):
            if result[i] == 2:
                result[i] = 0
        return result
    







damagingTarget = [[0.3,0.6,0.5],
                  [0.4,0.5,0.4],
                  [0.1,0.2,0.2]]

weaponTypes_numberOfInstances = {'Tank': 2 , 'Aircraft': 1 ,'Grenade': 2}
threatCoefficient = [16,5,10]
# numberOfTargets = len(threatCoefficient)

numberOfTypeWeapons = [weaponTypes_numberOfInstances[i] for i in weaponTypes_numberOfInstances]
# numberOfWeapons = sum(numberOfTypeWeapons)
# chromosomeSize = numberOfTargets * numberOfWeapons

ch1 = Chromosome(3,numberOfTypeWeapons,damagingTarget,threatCoefficient)

print(ch1.Genes)



def mutate(offspring1,offspring2,pm):
    arr = list()
    newArr = list()             # list of mutated offsprings
    arr.append(offspring1)
    arr.append(offspring2)

    for i in arr:
        newOffspring = list()
        for j in i:
            rm = random.random()
            if rm <= pm:
                if j == 1:
                    j = 0
                    newOffspring.append(j)
                else:
                    j = 1
                    newOffspring.append(j)
            else:
                newOffspring.append(j)
        newArr.append(newOffspring)
    return newArr

def checkConstraints(chromo,numOfW,numOfT):        #genes are weapons instances divided by targets
    counter = 0
    dividedChromo = list()
    totalNumOfW = numOfW*numOfT
    div = totalNumOfW/numOfT                             # total num of weapon instances per target
    while counter < len(chromo):
        divT = chromo[int(counter):int(div+counter)]                 # Each target has weapons from counter to div-1
        counter = counter + div
        dividedChromo.append(divT)

    counter2 = 0
    feasible = True
    while counter2 < len(dividedChromo[0]):         # loop over elements of a dividedChromo
        arrNum = 0
        while arrNum < len(dividedChromo)-1:            # loop over number of arrays in dividedChromo
            if dividedChromo[0][counter2] == dividedChromo[arrNum+1][counter2]:
                print("Chromosome is not feasible")
                feasible = False
                break
            else:
                arrNum = arrNum + 1
        if not feasible:
            break
        counter2 = counter2 + 1


def crossover(chromosome1, chromosome2, rc):
    r = random.uniform(0, 1)
    r = round(r, 1)

    if r < rc or r == rc:
        randomIndex = random.randint(1, len(chromosome1) - 1)
        print(randomIndex)
        offspring1 = chromosome1[0:randomIndex] + chromosome2[randomIndex:]
        offspring2 = chromosome2[0:randomIndex] + chromosome1[randomIndex:]
        return offspring1, offspring2
    else:
        print(r)
        return chromosome1, chromosome2


def Selection(chromosome1, chromosome2):
    return calculate_fitness(chromosome1) > calculate_fitness(chromosome2) ? chromosome1: chromosome2

#checkConstraints([1,1,0,1,0,0,0,1,0,1,0,0,0,1,1],5,3)
#offspring1 = [0,1,1,0,1]
#offspring2 = [1,1,1,0,0]
#print(mutate(offspring1,offspring2,0.3))
#print(crossover([1, 0, 1, 1], [0, 0, 0, 1], 0.8))

# A = [1,0,1,0,0  ,0,0,0,1,1,  0,1,0,0,0]
# print(Fitness(A))
# print(Representation())




# # 1
# [1, 0, 0, 0, 0,   
#  0, 0, 0, 0, 1,   
#  0, 1, 0, 1, 0]
# # 2
# [0, 0, 0, 0, 0,   
#  0, 1, 1, 0, 1,   
#  1, 0, 0, 1, 0]
# # 3
# [0, 0, 1, 0, 1,  
#  0, 1, 0, 0, 0,   
#  0, 0, 0, 0, 0]
# #  4
# [0, 1, 0, 0, 0,  
#  1, 0, 0, 0, 1,  
#  0, 0, 1, 1, 0]
# #  5
# [1, 1, 1, 0, 0,
#  0, 0, 0, 1, 0, 
#  0, 0, 0, 0, 0]