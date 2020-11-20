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

    def replaceGeneration(self,oldGeneration,newGeneration):
        pass

    def Selection(self, generation, sizeOfMatingPool):
        mating_pool = []
        for i in range(sizeOfMatingPool):
            random_index1 = random.randint(0, len(generation) // 2)
            random_index2 = random.randint((len(generation) // 2) + 1, len(generation) - 1)

            chosen_chromosome = Chromosome(generation[random_index1].Genes,
                                           generation[random_index1].numberOfChannels,
                                           generation[random_index1].totalBudget)
            print(random_index1,"i:", i)
            print(random_index2,"i:", i)
            if generation[random_index2].fitness >= generation[random_index1].fitness:
                chosen_chromosome = Chromosome(generation[random_index2].Genes,
                                               generation[random_index2].numberOfChannels,
                                               generation[random_index2].totalBudget)
            mating_pool.append(chosen_chromosome)

        return mating_pool

    def crossover(self, chromosome1, chromosome2, rc):
        r = random.uniform(0, 1)
        r = round(r, 1)
        if r <= rc:
            random_index1 = random.randint(1, len(chromosome1.Genes) // 2)
            random_index2 = random.randint((len(chromosome1.Genes) // 2) + 1, len(chromosome1.Genes) - 1)

            print(random_index1)

            print(random_index2)
            genesOffspring1 = chromosome1.Genes[:random_index1] + chromosome2.Genes[
                                                                  random_index1:random_index2] + chromosome1.Genes[
                                                                                                 random_index2:]
            genesOffspring2 = chromosome2.Genes[:random_index1] + chromosome1.Genes[
                                                                  random_index1:random_index2] + chromosome2.Genes[
                                                                                                 random_index2:]
            chromosome1.SetGenes(genesOffspring1)
            chromosome2.SetGenes(genesOffspring2)
            return chromosome1, chromosome2
        else:
            return chromosome1, chromosome2

    def uniformMutation(self, offspring, pm):
        arr = offspring.Genes[:]
        newOffspring = list()
        for gene in arr:
            rm = random.random()
            if rm <= pm:
                deltaLower = gene.allocatedBudgetValue - float(gene.lowerBound)
                deltaUpper = (float(gene.upperBound)*offspring.totalBudget)/100 - gene.allocatedBudgetValue

                r1 = random.random()
                delta = 0
                if r1 <= 0.5:
                    delta = deltaLower
                elif r1 > 0.5:
                    delta = deltaUpper

                r2 = random.uniform(0,delta)
                if delta == deltaLower:
                    newValue = gene.allocatedBudgetValue - r2
                elif delta == deltaUpper:
                    newValue = gene.allocatedBudgetValue + r2

                gene.allocatedBudgetValue = newValue
                newOffspring.append(gene)
            else:
                newOffspring.append(gene)
        offspring.SetGenes(newOffspring)
        return offspring

    def nonUniformMutation(self, offspring, t, T, b, pm):          # t: current gen number, T: max number of gens, b: non-uniformity factor
        arr = offspring.Genes[:]
        newOffspring = list()
        for gene in arr:
            rm = random.random()
            if rm <= pm:
                deltaLower = gene.allocatedBudgetValue - float(gene.lowerBound)
                deltaUpper = (float(gene.upperBound)*offspring.totalBudget)/100 - gene.allocatedBudgetValue

                r1 = random.random()
                y = 0
                if r1 <= 0.5:
                    y = deltaLower
                elif r1 > 0.5:
                    y = deltaUpper

                r = random.random()                     # to be used in Δ(t,y) eq.
                delta_t_y = y * (1-pow(r,pow((1-t/T),b)))
                if y == deltaLower:
                    newValue = gene.allocatedBudgetValue - delta_t_y
                elif y == deltaUpper:
                    newValue = gene.allocatedBudgetValue + delta_t_y

                gene.allocatedBudgetValue = newValue
                newOffspring.append(gene)
            else:
                newOffspring.append(gene)
        offspring.SetGenes(newOffspring)
        return offspring

    def checkConstraints(self, chromo, totalBudget):
        genes = chromo.Genes[:]
        sum = 0
        for i in genes:
            sum += i.allocatedBudgetValue
        for i in genes:
            if sum > totalBudget or i.allocatedBudgetValue < float(i.lowerBound) or\
                    i.allocatedBudgetValue > (float(i.upperBound)*totalBudget)/100:
                return False

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
    numberOfChannels = 0

    def __init__(self, Genes, numberOfChannels,totalBudget):
        self.numberOfChannels = numberOfChannels
        self.totalBudget = totalBudget
        self.Genes = Genes
        self.fitness = self.Fitness()

    def SetGenes(self, genes):
        self.Genes = genes
        self.Fitness()

    def Fitness(self):
        for g in self.Genes:
            self.fitness += (g.allocatedBudgetValue * g.ROI) / self.totalBudget

    def showChromosome(self):
        d = []
        for gene in self.Genes:
            d.append(gene.allocatedBudgetValue)
        print(d, " Fitness : ", self.fitness)

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

    # gene1 = Gene()
    # gene1.allocatedBudgetValue = 36
    # gene1.lowerBound = 2.7
    # gene1.upperBound = 58
    #
    # gene2 = Gene()
    # gene2.allocatedBudgetValue = 50
    # gene2.lowerBound = 20.5
    # gene2.upperBound = 60
    # genesList = [gene1,gene2]
    #
    # chromo = Chromosome(genesList,4,100)
    # ga = GeneticA(0.5,0.1)
    # ga.checkConstraints(chromo,100)
    # ga.nonUniformMutation(chromo,1,5,1,0.5)







