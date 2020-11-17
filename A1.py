import random


def DividedChromosome(chromo, numOfW, numOfT):
    counter = 0
    dividedChromo = list()
    totalNumOfW = numOfW * numOfT
    div = totalNumOfW / numOfT  # total num of weapon instances per target
    while counter < len(chromo):
        divT = chromo[int(counter):int(div + counter)]  # Each target has weapons from counter to div-1
        counter = counter + div
        dividedChromo.append(divT)
    return dividedChromo


def Representation(numberOfTargets , numberOfInstanceWeapons):
    result = []
    temp = []
    for i in range(numberOfTargets):
        for j in range(numberOfInstanceWeapons):
            if i == 0:
                rand = random.randint(0, 1)
                temp.append(rand)
            else:
                if temp[j] == 0:
                    rand = random.randint(0, 1)
                    temp[j] = rand
        result += temp
        # print("before" , temp)
        for i in range(len(temp)):
            if temp[i] == 1: temp[i] = 2
    for i in range(len(result)):
        if result[i] == 2:
            result[i] = 0
    return result


class GeneticA:
    finalResult = 0
    generation = []
    probOfCross = 0.0
    probOfMutate = 0.0

    def __init__(self, probOfCross, probOfMutate):
        self.probOfCross = probOfCross
        self.probOfMutate = probOfMutate

    def CreateNewGeneration(self, generation):

        self.generation = generation[:]
        n1 = random.randint(0, len(generation) // 2)
        n2 = random.randint(len(generation) // 2 + 1, len(generation) - 1)
        first, newIndex1 = self.Selection(generation[n1], n1, generation[n2], n2)
        n3 = random.randint(0, len(generation) // 2 + 1)
        n4 = random.randint(len(generation) // 2, len(generation) - 1)
        second, newIndex2 = self.Selection(generation[n3], n3, generation[n4], n4)

        offSpring1, offSpring2 = self.crossover(first, second, self.probOfCross)

        offSpring1 = self.mutate(offSpring1, self.probOfMutate)
        offSpring2 = self.mutate(offSpring2, self.probOfMutate)

        isFeasible = self.checkConstraints(offSpring1, generation[0].numberOfInstanceWeapons,
                                           generation[0].numberOfTargets)
        if not isFeasible: offSpring1 = self.fixChromosome(offSpring1)
        isFeasible = self.checkConstraints(offSpring2, generation[0].numberOfInstanceWeapons,
                                           generation[0].numberOfTargets)
        if not isFeasible: offSpring2 = self.fixChromosome(offSpring2)

        offSpring1.SetGenes(offSpring1.Genes)
        offSpring2.SetGenes(offSpring2.Genes)

        if generation[newIndex1].fitness > offSpring1.fitness:
            generation[newIndex1] = offSpring1
        if generation[newIndex2].fitness > offSpring2.fitness:
            generation[newIndex2] = offSpring2

        newGeneration = generation[:]

        return newGeneration

    def Selection(self, chromosome1, n1, chromosome2, n2):
        if chromosome1.fitness < chromosome2.fitness:
            new = Chromosome(chromosome1.Genes, chromosome1.numberOfTargets, chromosome1.numberOfTypeWeapons,
                             chromosome1.damagingTarget, chromosome1.threatCoefficient)
            return new, n1
        else:
            new2 = Chromosome(chromosome2.Genes, chromosome2.numberOfTargets, chromosome2.numberOfTypeWeapons,
                              chromosome2.damagingTarget, chromosome2.threatCoefficient)
            return new2, n2

    def crossover(self, chromosome1, chromosome2, rc):
        r = random.uniform(0, 1)
        r = round(r, 1)
        if r <= rc:
            randomIndex = random.randint(1, len(chromosome1.Genes) - 1)
            genesOffspring1 = chromosome1.Genes[0:randomIndex] + chromosome2.Genes[randomIndex:]
            genesOffspring2 = chromosome2.Genes[0:randomIndex] + chromosome1.Genes[randomIndex:]
            chromosome1.SetGenes(genesOffspring1)
            chromosome2.SetGenes(genesOffspring2)
            return chromosome1, chromosome2
        else:
            return chromosome1, chromosome2

    def mutate(self, offspring, pm):
        arr = offspring.Genes[:]
        newOffspring = list()
        for i in arr:
            rm = random.random()
            if rm <= pm:
                if i == 1:
                    newOffspring.append(0)
                else:
                    newOffspring.append(1)
            else:
                newOffspring.append(i)
        offspring.SetGenes(newOffspring)
        return offspring

    def checkConstraints(self, chromo, numOfW, numOfT):  # genes are weapons instances divided by targets
        counter = 0
        dividedChromo = DividedChromosome(chromo.Genes, numOfW, numOfT)

        counter2 = 0
        feasible = True
        while counter2 < len(dividedChromo[0]):  # loop over elements of a dividedChromo
            arrNum = 0
            while arrNum < len(dividedChromo) - 1:  # loop over number of arrays in dividedChromo
                if dividedChromo[0][counter2] == dividedChromo[arrNum + 1][counter2]:
                    # print("Chromosome is not feasible")
                    feasible = False
                    return feasible
                else:
                    arrNum = arrNum + 1
            if not feasible:
                return feasible
            counter2 = counter2 + 1

    def fixChromosome(self, chromosome):
        temp = []
        result = []
        threatCoefficient = chromosome.threatCoefficient
        dictOfThreatCoefficient = {index: value for index, value in enumerate(threatCoefficient)}
        sortedThreatCoefficient = sorted(dictOfThreatCoefficient.items(), key=
        lambda kv: (kv[1], kv[0]))

        dividedChromo = DividedChromosome(chromosome.Genes, chromosome.numberOfInstanceWeapons,
                                          chromosome.numberOfTargets)
        for j in range(chromosome.numberOfTargets - 1):
            if j == 0:
                temp = dividedChromo[sortedThreatCoefficient[j][0]]
                temp3 = temp[:]
                result.append(temp3)
            for i in range(len(temp)):
                if temp[i] == 1:
                    temp[i] = 2
            temp2 = dividedChromo[sortedThreatCoefficient[j + 1][0]]
            for i in range(len(temp)):
                if temp2[i] == 1 and temp[i] == 0:
                    temp[i] = 1
            temp3 = temp[:]
            result.append(temp3)

        for i in range(len(result)):
            for j in range(len(result[0])):
                if result[i][j] == 2:
                    result[i][j] = 0

        tempResult = result[:]
        for i in range(len(sortedThreatCoefficient)):
            tempResult[sortedThreatCoefficient[i][0]] = result[i]
        finalResult = []
        for i in range(len(sortedThreatCoefficient)):
            finalResult += tempResult[i]
        chromosome.SetGenes(finalResult)
        return chromosome


class Chromosome:
    Genes = []
    numberOfTargets = 0
    numberOfTypeWeapons = []
    damagingTarget = []
    threatCoefficient = []
    survivingTarget = []
    numberOfInstanceWeapons = 0
    fitness = 0

    def __init__(self, Genes, numberOfTargets, numberOfTypeWeapons, damagingTarget, threatCoefficient):
        self.numberOfTargets = numberOfTargets
        self.numberOfTypeWeapons = numberOfTypeWeapons
        self.damagingTarget = damagingTarget
        self.threatCoefficient = threatCoefficient
        self.numberOfInstanceWeapons = sum(self.numberOfTypeWeapons)
        self.survivingTarget = self.CalculateSurvivingTarget()
        self.Genes = Genes
        self.fitness = self.Fitness()

    def SetGenes(self, Genes):
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
                if self.Genes[index] == 1:
                    temp *= self.survivingTarget[indexOfInstance][i]
                index += 1
                if tempInstance[indexOfInstance] > 1:
                    tempInstance[indexOfInstance] -= 1
                else:
                    indexOfInstance += 1
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



if __name__ == '__main__':

    print('Assignment 1 – Weapon Target Assignment Problem (WTA) By Mariam & Ahmed & Moaaz ')
    print('********************************************************************************')
    print('Enter the weapon types and the number of instances of each type: (Enter “x” when you’re done)')

    key = ''
    weaponTypes_numberOfInstances = dict()


    while key != 'x':
        key = input()
        key_value = key.split(" ")
        if len(key_value) > 1:
            weaponTypes_numberOfInstances[key_value[0]] = int(key_value[1])

    numberOfWeaponTypes = len(weaponTypes_numberOfInstances)
    numberOfInstancesPerWeapon = [weaponTypes_numberOfInstances[i] for i in weaponTypes_numberOfInstances]
    numberOfWeapons = sum(numberOfInstancesPerWeapon)
    numberOfTargets = int(input("Enter number of targets: "))

    threatCoefficient = list()
    print('********************************************************************************')
    print("Enter the threat coefficient of each target: ")
    for i in range(numberOfTargets):
        threatCoefficient.append(int(input()))
    print('********************************************************************************')
    # print("Enter the weapons’ success probabilities matrix: ")
    # damagingTarget = []
    # for i in range(numberOfTargets):
    #     lst = list()
    #     damagingTarget.append(lst)
    #     for j in range(numberOfWeaponTypes):
    #         lst.append(float(input()))
    damagingTarget = [[0.3,0.6,0.5],
                      [0.4,0.5,0.4],
                      [0.1,0.2,0.2]]

    print('********************************************************************************')
    print("Output of WTA Problem : ")
    chromosomeSize = numberOfTargets * numberOfWeapons
    chromosomeList1 = []
    for i in range(5):
        Genes = Representation(numberOfTargets, sum(numberOfInstancesPerWeapon))
        ch1 = Chromosome(Genes, numberOfTargets, numberOfInstancesPerWeapon, damagingTarget, threatCoefficient)
        chromosomeList1.append(ch1)

    n = 0
    while n < 50:
        ga = GeneticA(0.7 , 0.1)
        chromosomeList2 = ga.CreateNewGeneration(chromosomeList1)
        n += 1

    minChromosome = chromosomeList2[0]
    for i in chromosomeList2:
        # print(i.Genes, i.fitness)
        if i.fitness < minChromosome.fitness:
            minChromosome = i
    dividedMinChromosome = DividedChromosome(minChromosome.Genes, numberOfWeapons , numberOfTargets)
    count = 0
    target = 0
    for i in dividedMinChromosome:
        for x, y in weaponTypes_numberOfInstances.items():
            for j in range(y):
                if i[count] == 1:
                    print(x ,  'number ', j  , 'is assigned to target ' , 'number ' , target)
                if count == numberOfWeapons - 1:
                    count = 0
                else:
                    count += 1
        target += 1

    print('\n \n \n The expected total threat of the surviving targets is ' , minChromosome.fitness)










