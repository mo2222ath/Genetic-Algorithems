import random

def Representation(numberOfChannels, ROIDictionary, boundariesList, totalBudget):
    pass



class GeneticA:
    finalResult = 0
    generation = []
    probOfCross = 0.0
    probOfMutate = 0.0

    def __init__(self, probOfCross, probOfMutate):
        self.probOfCross = probOfCross
        self.probOfMutate = probOfMutate

    def CreateNewGeneration(self, generation):
        pass

    def replaceGeneration(self,oldGeneration,newGeneration):
        pass

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
        pass

    def uniformMutation(self, offspring, pm):
        pass

    def nonUniformMutation(self, offspring, pm):
        pass

    def checkConstraints(self, chromo, numOfW, numOfT) # genes are weapons instances divided by targets
        pass

    def fixChromosome(self, chromosome):
        pass

class Gene:
    ROI = 0
    allocatedBudgetValue = 0.0
    channelName = ""
    upperBound = ""
    lowerBound = ""

class Chromosome:
    Genes = []
    numberOfChannels = 0
    totalBudget = 0
    fitness = 0

    def __init__(self, Genes, numberOfChannels,totalBudget):
        self.numberOfChannels = numberOfChannels
        self.totalBudget = totalBudget
        self.Genes = Genes
        self.fitness = self.Fitness()

    def SetGenes(self, Genes):
        self.Genes = Genes
        self.fitness = self.Fitness()

    def Fitness(self):
        pass

if __name__ == '__main__':
    print("Enter the marketing budget (in thousands): ")
    totalBudget = float(input())

    print("Enter the number of marketing channels: ")
    numberOfChannels = int(input())

    print("Enter the name and ROI (in %) of each channel separated by space: ")
    key = ""
    ROIDictionary = dict()
    for i in range(numberOfChannels):
        key = input()
        key_value = key.split(" ")
        if len(key_value) > 1:
            ROIDictionary[key_value[0:len(key_value)-2]] = int(key_value[-1])


    print("Enter the lower (k) and upper bounds (%) of investment in each channel: (enter x if there is no bound)")
    boundariesList = list()
    for i in range(numberOfChannels):
        line = input()
        line = line.split(" ")
        boundariesList.append(line)

    print("Output of GA: \n")
    chromosmeList1 = []
    for i in range(5):
        Genes = Representation(numberOfChannels,ROIDictionary,boundariesList,totalBudget)
        ch1 = Chromosome(Genes,numberOfChannels,totalBudget)
        chromosmeList1.append(ch1)

    print("First Gener")
    for i in chromosmeList1:
        print(i.Genes , i.fitness)

    n = 0
    while n < 5000:
        ga = GeneticA(0.5 , 0.3)
        chromosmeList2 = ga.CreateNewGeneration(chromosmeList1)
        n += 1
        print("iteration ",n)
        print("Second Gener")
        for i in chromosmeList2:
            print(i.Genes , i.fitness)






# Constraints
    # 1: sum of genes <= total budget





