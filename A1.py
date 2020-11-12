import random

def CalculateSurvivingTarget(damagingTarget):
    SurvivingTarget = []
    for i in range(len(damagingTarget)):
        temp = damagingTarget[i]
        temp2 = []
        for j in range(len(damagingTarget[0])):
            temp2.append(1.0 - temp[j])
        SurvivingTarget.append(temp2)
    return SurvivingTarget

damagingTarget = [[0.3,0.6,0.5],
                  [0.4,0.5,0.4],
                  [0.1,0.2,0.2]]

weaponTypes_numberOfInstances = {'Tank': 2 , 'Aircraft': 1 ,'Grenade': 2}
threatCoefficient = [16,5,10]
numberOfTargets = len(threatCoefficient)
survivingTarget = CalculateSurvivingTarget(damagingTarget)
numberOfInstances = [weaponTypes_numberOfInstances[i] for i in weaponTypes_numberOfInstances]
numberOfWeapons = sum(numberOfInstances)
chromosomeSize = numberOfTargets * numberOfWeapons


def Fitness(A):
    numberOfGenes = len(A)
    nummberOfWappens = numberOfGenes // numberOfTargets
    index = 0
    result = 0
    for i in range(numberOfTargets):
        tempInstance = numberOfInstances[:]
        indexOfInstance = 0
        temp = 1
        for j in range(nummberOfWappens):
            if A[index] == 1 :
                temp *= survivingTarget[indexOfInstance][i]
            index += 1
            if tempInstance[indexOfInstance] > 1 :
                tempInstance[indexOfInstance] -=1
            else:
                indexOfInstance +=1
        temp *= threatCoefficient[i]
        result += temp
    return result


def Representation():
    result = []
    temp = []
    for i in range(numberOfTargets):
        for j in range(numberOfWeapons):
            if i==0:
                n = random.randint(0,1)
                temp.append(n)
            else:
                if temp[j] == 0:
                    n = random.randint(0,1)
                    temp[j] = n
        result += temp
        print("before" , temp)
        for i in range(len(temp)):
            if temp[i] == 1: temp[i] = 2
        print("After" , temp)
        print(result)
    for i in range(len(result)):
        if result[i] == 2:
            result[i] = 0
    return result


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