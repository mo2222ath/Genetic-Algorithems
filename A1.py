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

    def __init__(self,Genes,numberOfTargets,numberOfTypeWeapons,damagingTarget,threatCoefficient):        
        self.numberOfTargets = numberOfTargets
        self.numberOfTypeWeapons = numberOfTypeWeapons
        self.damagingTarget = damagingTarget
        self.threatCoefficient = threatCoefficient
        self.numberOfInstanceWeapons = sum(self.numberOfTypeWeapons)
        self.survivingTarget = self.CalculateSurvivingTarget()
        self.Genes = Genes
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
numberOfTargets = len(threatCoefficient)

numberOfTypeWeapons = [weaponTypes_numberOfInstances[i] for i in weaponTypes_numberOfInstances]
# numberOfWeapons = sum(numberOfTypeWeapons)
# chromosomeSize = numberOfTargets * numberOfWeapons

ch1 = Chromosome(numberOfTargets,numberOfTypeWeapons,damagingTarget,threatCoefficient)

print(ch1.Genes , ch1.fitness)


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