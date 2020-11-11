
DamagingTarget = [[0.3,0.6,0.5],
                  [0.4,0.5,0.4],
                  [0.1,0.2,0.2]]

weaponTypes_numberOfInstances = {'Tank': 2 , 'Aircraft': 1 ,'Grenade': 2}
threatCoefficient = [16,5,10]

def CalculateSurvivingTarget(DamagingTarget):
    SurvivingTarget = []
    for i in range(len(DamagingTarget)):
        temp = DamagingTarget[i]
        temp2 = []
        for j in range(len(DamagingTarget[0])):
            temp2.append(1.0 - temp[j])
        SurvivingTarget.append(temp2)
    return SurvivingTarget


def fitness(A):
    NumberOfTargets = len(threatCoefficient)
    NumberOfGenes = len(A)
    NummberOfWappens = NumberOfGenes // NumberOfTargets
    SurvivingTarget = CalculateSurvivingTarget(DamagingTarget)
    numberOfInstances = [weaponTypes_numberOfInstances[i] for i in weaponTypes_numberOfInstances]
    index = 0
    result = 0
    for i in range(NumberOfTargets):
        tempInstance = numberOfInstances[:]
        indexOfInstance = 0
        temp = 1
        for j in range(NummberOfWappens):
            if(A[index] == 1):
                temp *= SurvivingTarget[indexOfInstance][i]
            index += 1
            if(tempInstance[indexOfInstance] > 1):
                tempInstance[indexOfInstance] -=1
            else:
                indexOfInstance +=1
        temp *= threatCoefficient[i]
        result += temp
    return result



A = [1,0,1,0,0  ,0,0,0,1,1,  0,1,0,0,0]

print(fitness(A))