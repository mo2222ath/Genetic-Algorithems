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

    def CreateNewGeneration(self, generation, isUniform, t, sizeOfGeneration):
        self.generation = generation[:]

        matingPool = self.Selection(self.generation, len(self.generation) // 2)

        n1 = random.randint(0, len(matingPool) // 2)
        n2 = random.randint(len(matingPool) // 2 + 1, len(matingPool) - 1)

        first, second = matingPool[n1], matingPool[n2]
        offSpring1, offSpring2 = self.crossover(first, second, self.probOfCross)

        if isUniform:
            offSpring1 = self.uniformMutation(offSpring1, self.probOfMutate)
            offSpring2 = self.uniformMutation(offSpring2, self.probOfMutate)
        else:
            offSpring1 = self.nonUniformMutation(offSpring1, t, sizeOfGeneration, 1, self.probOfMutate)
            offSpring2 = self.nonUniformMutation(offSpring2, t, sizeOfGeneration, 1, self.probOfMutate)

        isFeasible = self.checkConstraints(offSpring1, offSpring1.totalBudget)
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

    def replaceGeneration(self, oldGeneration, newGeneration):
        pass

    def Selection(self, generation, sizeOfMatingPool):
        mating_pool = []
        for i in range(sizeOfMatingPool):
            random_index1 = random.randint(0, len(generation) // 2)
            random_index2 = random.randint((len(generation) // 2) + 1, len(generation) - 1)

            chosen_chromosome = Chromosome(generation[random_index1].Genes,
                                           generation[random_index1].numberOfChannels,
                                           generation[random_index1].totalBudget)
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
            temp1 = chromosome1.Genes[:]
            temp2 = chromosome2.Genes[:]

            offspring1 = Chromosome(temp1 , chromosome1.numberOfChannels , chromosome1.totalBudget)
            offspring2 = Chromosome(temp2 , chromosome1.numberOfChannels , chromosome1.totalBudget)
            print("***********before")
            chromosome1.showChromosome()
            chromosome2.showChromosome()
            offspring1.showChromosome()
            offspring2.showChromosome()

            for i in range(random_index1, random_index2 + 1):
                offspring1.Genes[i].allocatedBudgetValue = chromosome2.Genes[i].allocatedBudgetValue
                offspring2.Genes[i].allocatedBudgetValue = chromosome1.Genes[i].allocatedBudgetValue
            print("***********after")
            chromosome1.showChromosome()
            chromosome2.showChromosome()
            offspring1.showChromosome()
            offspring2.showChromosome()
            print("***********end")

            offspring1.updateFitness()
            offspring2.updateFitness()
            return offspring1, offspring2
        else:
            return chromosome1, chromosome2

    def uniformMutation(self, offspring, pm):
        arr = offspring.Genes[:]
        newOffspring = list()
        for gene in arr:
            rm = random.random()
            if rm <= pm:
                deltaLower = gene.allocatedBudgetValue - float(gene.lowerBound)
                deltaUpper = (float(gene.upperBound) * offspring.totalBudget) / 100 - gene.allocatedBudgetValue

                r1 = random.random()
                delta = 0
                if r1 <= 0.5:
                    delta = deltaLower
                elif r1 > 0.5:
                    delta = deltaUpper

                r2 = random.uniform(0, delta)
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

    def nonUniformMutation(self, offspring, t, T, b,
                           pm):  # t: current gen number, T: max number of gens, b: non-uniformity factor
        arr = offspring.Genes[:]
        newOffspring = list()
        for gene in arr:
            rm = random.random()
            if rm <= pm:
                deltaLower = gene.allocatedBudgetValue - float(gene.lowerBound)
                deltaUpper = (float(gene.upperBound) * offspring.totalBudget) / 100 - gene.allocatedBudgetValue

                r1 = random.random()
                y = 0
                if r1 <= 0.5:
                    y = deltaLower
                elif r1 > 0.5:
                    y = deltaUpper

                r = random.random()  # to be used in Δ(t,y) eq.
                delta_t_y = y * (1 - pow(r, pow((1 - t / T), b)))
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
        for gene in genes:
            sum += gene.allocatedBudgetValue
        for gene in genes:
            if sum > totalBudget or gene.allocatedBudgetValue < float(gene.lowerBound) or \
                    gene.allocatedBudgetValue > (float(gene.upperBound) * totalBudget) / 100:
                return False
        return True

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

    def __init__(self, Genes, numberOfChannels, totalBudget):
        self.numberOfChannels = numberOfChannels
        self.totalBudget = totalBudget
        self.Genes = Genes[:]
        self.Fitness()

    def SetGenes(self, genes):
        self.Genes = genes[:]
        self.Fitness()

    def updateFitness(self):
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

    # print("Output of GA: \n")
    chromosmeList1 = []
    for i in range(5):
        Genes = Representation(ROIDictionary, boundariesList, totalBudget)
        ch1 = Chromosome(Genes, numberOfChannels, totalBudget)
        chromosmeList1.append(ch1)

    print("First Generation : ")
    for chromosome in chromosmeList1:
        chromosome.showChromosome()

    g = GeneticA(0.5 , 0.01)

    n1 , n2 = g.crossover(chromosmeList1[0] , chromosmeList1[1] , 0.5)
    print("Cross")
    n1.showChromosome()
    n2.showChromosome()

    # n = 0
    # isUniform  = True
    # sizeOfGeneration = 5000
    # while n < sizeOfGeneration:
    #     ga = GeneticA(0.5 , 0.3)
    #     chromosmeList2 = ga.CreateNewGeneration(chromosmeList1 , isUniform , n , sizeOfGeneration)
    #     n += 1
    #     print("iteration ",n)
    #     print("Second Gener")
    #     for i in chromosmeList2:
    #         print(i.Genes , i.fitness)

    # l1 = [1.0 , 2.0 , 3.0 , 4.0]
    # l2 = [5.0 , 6.0 , 7.0 , 8.0]
    # ch1 = Chromosome(l1, 4 , 100)
    # ch2 = Chromosome(l2, 4, 100)
    # n1 , n2 = GeneticA.crossover(ch1,ch2,0.5)
    # n1.showChromosome()
    # n2.showChromosome()

# Constraints
# 1: sum of genes <= total budget

# gene1 = Gene()
# gene1.allocatedBudgetValue = 1
#
# gene2 = Gene()
# gene2.allocatedBudgetValue = 2
#
# gene3 = Gene()
# gene3.allocatedBudgetValue = 3
#
#
# gene4 = Gene()
# gene4.allocatedBudgetValue = 4
# genesList = [gene1,gene2 , gene3 , gene4]
#
# chromo = Chromosome(genesList,4,100)
# ga = GeneticA(0.5,0.1)
# ga.checkConstraints(chromo,100)
# ga.nonUniformMutation(chromo,1,5,1,0.5)
