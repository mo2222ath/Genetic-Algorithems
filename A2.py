import random


def Representation(ROIDictionary, boundariesList, totalBudget):
    copyBoundariesList = boundariesList[:]
    copyROIDictionary = ROIDictionary
    allowedBudget = 0
    lowerSum = 0
    genes = []
    channelsNames = list(ROIDictionary.keys())
    channelsRIO = list(ROIDictionary.values())
    c = 0
    for item in copyBoundariesList:
        gene = Gene()
        if item[0] == 'x':
            item[0] = 0
        if item[1] == 'x':
            item[1] = 0
        item[1] = (item[1] / 100) * totalBudget
        lowerSum += item[0]
        gene.lowerBound = item[0]
        gene.upperBound = item[1]
        gene.ROI = channelsRIO[c]
        gene.channelName = channelsNames[c]
        c += 1
        genes.append(gene)

    allowedBudget = totalBudget - lowerSum

    for gene in genes:
        if gene.upperBound == 0:
            gene.upperBound = gene.lowerBound + allowedBudget
        elif allowedBudget < gene.upperBound:
            gene.upperBound = allowedBudget
        gene.allocatedBudgetValue = random.uniform(int(gene.lowerBound), int(gene.upperBound))
        allowedBudget = allowedBudget - (gene.allocatedBudgetValue - gene.lowerBound)

    # for item in genes:
    #     print(item.channelName ,item.lowerBound , item.upperBound , item.allocatedBudgetValue )
    return genes


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

    def replaceGeneration(self, oldGeneration, newGeneration):
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

    def checkConstraints(self, chromo, numOfW, numOfT):
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
    totalBudget = 0
    fitness = 0

    def __init__(self, genes, numberOfChannel, totalBudgets):
        self.numberOfChannels = numberOfChannel
        self.totalBudget = totalBudgets
        self.Genes = genes
        self.Fitness()

    def SetGenes(self, genes):
        self.Genes = genes
        self.Fitness()

    def Fitness(self):
        for g in self.Genes:
            self.fitness += (g.allocatedBudgetValue * g.ROI) / totalBudget
            # print(self.fitness, g.allocatedBudgetValue, g.ROI, totalBudget)

    def showChromosome(self):
        d = []
        for gene in self.Genes:
            d.append(gene.allocatedBudgetValue)
        print(d , " Fitness : " , self.fitness)


if __name__ == '__main__':
    print("Enter the marketing budget (in thousands): ")
    totalBudget = 100  # float(input())

    print("Enter the number of marketing channels: ")
    numberOfChannels = 4  # int(input())

    print("Enter the name and ROI (in %) of each channel separated by space: ")
    key = ""
    ROIDictionary = {"TV advertising": 8, "Google": 12, "Twitter": 7, "Facebook": 11}  # dict()
    # for i in range(numberOfChannels):
    #     key = input()
    #     key_value = key.split(" ")
    #     if len(key_value) > 1:
    #         tempKey = key_value[0:len(key_value) - 1]
    #         s = ''
    #         for item in tempKey:
    #             s += ' ' + item
    #         ROIDictionary[s] = int(key_value[-1])

    print("Enter the lower (k) and upper bounds (%) of investment in each channel: (enter x if there is no bound)")
    boundariesList = [[2.7, 58], [20.5, 'x'], ['x', 18], [10, 'x']]
    # for i in range(numberOfChannels):
    #     line = input()
    #     line = line.split(" ")
    #     if line[0] != 'x':
    #         line[0] = float(line[0])
    #     if line[1] != 'x':
    #         line[1] = float(line[1])
    #     boundariesList.append(line)

    print("Output of GA: \n")
    chromosmeList1 = []
    for i in range(5):
        Genes = Representation(ROIDictionary, boundariesList, totalBudget)
        ch1 = Chromosome(Genes, numberOfChannels, totalBudget)
        chromosmeList1.append(ch1)

    print("First Generation : ")
    for chromosome in chromosmeList1:
        chromosome.showChromosome()


    # n = 0
    # while n < 5000:
    #     ga = GeneticA(0.5 , 0.3)
    #     chromosmeList2 = ga.CreateNewGeneration(chromosmeList1)
    #     n += 1
    #     print("iteration ",n)
    #     print("Second Gener")
    #     for i in chromosmeList2:
    #         print(i.Genes , i.fitness)

# Constraints
# 1: sum of genes <= total budget
