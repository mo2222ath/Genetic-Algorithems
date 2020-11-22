import random
import copy


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
        n2 = random.randint((len(matingPool) // 2) , len(matingPool) - 1)

        first, second = matingPool[n1], matingPool[n2]
        offSpring1, offSpring2 = self.crossover(first, second, self.probOfCross)

        if isUniform:
            offSpring1 = self.uniformMutation(offSpring1, self.probOfMutate)
            offSpring2 = self.uniformMutation(offSpring2, self.probOfMutate)

        else:
            offSpring1 = self.nonUniformMutation(offSpring1, t, sizeOfGeneration, 1, self.probOfMutate)
            offSpring2 = self.nonUniformMutation(offSpring2, t, sizeOfGeneration, 1, self.probOfMutate)


        if not self.checkTotalBudgetConstraints(offSpring1):
            self.fixChromosome(offSpring1)

        if not self.checkTotalBudgetConstraints(offSpring2):
            self.fixChromosome(offSpring2)


        for ch in generation:
            if not self.checkTotalBudgetConstraints(ch):
                self.fixChromosome(ch)

        newGeneration = self.replaceGeneration(generation , offSpring1 , offSpring2)

        return newGeneration

    def replaceGeneration(self, oldGeneration, offSpring1 , offSpring2):
        newGeneration = copy.deepcopy(oldGeneration)
        newGeneration.append(offSpring1)
        newGeneration.append(offSpring2)
        fitnessList = []
        for chromosome in newGeneration:
            fitnessList.append(chromosome.fitness)
        for i in range(2):
            indexMin = fitnessList.index(min(fitnessList))
            fitnessList.remove(fitnessList[indexMin])
            newGeneration.remove(newGeneration[indexMin])

        return newGeneration

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

            # print(random_index1)
            # print(random_index2)

            offspring1 = copy.deepcopy(chromosome1)
            offspring2 = copy.deepcopy(chromosome2)

            for i in range(random_index1, random_index2 + 1):
                offspring1.Genes[i].allocatedBudgetValue = chromosome2.Genes[i].allocatedBudgetValue
                offspring2.Genes[i].allocatedBudgetValue = chromosome1.Genes[i].allocatedBudgetValue

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
        offspring.updateFitness()
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
        offspring.updateFitness()
        return offspring

    def checkTotalBudgetConstraints(self, chromo):
        if chromo.totalBudgetChromosome > chromo.totalBudget:
            return False
        return True

    def calculateTotalBudget(self,chromo):
        genes = chromo.Genes[:]
        tempSum = 0
        for gene in genes:
            tempSum += gene.allocatedBudgetValue
        return tempSum

    def fixChromosome(self, chromosome):
        total = copy.deepcopy(chromosome.totalBudgetChromosome)
        diff = total - chromosome.totalBudget
        ROIList = []
        for item in chromosome.Genes:
            ROIList.append(item.ROI)
        while diff != 0:
            minROI = min(ROIList)
            indexMin = ROIList.index(minROI)
            ROIList[indexMin] = 1000000
            if chromosome.Genes[indexMin].allocatedBudgetValue <= diff:
                diff -= chromosome.Genes[indexMin].allocatedBudgetValue
                chromosome.Genes[indexMin].allocatedBudgetValue = 0
            else:
                chromosome.Genes[indexMin].allocatedBudgetValue -= diff
                diff = 0
        chromosome.updateFitness()







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
    totalBudgetChromosome = 0

    def __init__(self, genes, numberOfChannels, totalBudget):
        self.numberOfChannels = numberOfChannels
        self.totalBudget = totalBudget
        self.Genes = genes[:]
        self.Fitness()
        self.totalBudgetChromosome = self.calculateTotalBudget()

    def SetGenes(self, genes):
        self.Genes = genes[:]
        self.Fitness()

    def updateFitness(self):
        self.fitness = 0.0
        self.Fitness()
        self.totalBudgetChromosome = self.calculateTotalBudget()

    def Fitness(self):
        for g in self.Genes:
            self.fitness += (g.allocatedBudgetValue * g.ROI) / self.totalBudget

    def showChromosome(self):
        d = []
        for gene in self.Genes:
            d.append(gene.allocatedBudgetValue)
            t = (gene.lowerBound , gene.upperBound)
            d.append(t)
        print(d)
        print(" Fitness : ", self.fitness)
        print("Total budget" , self.totalBudgetChromosome)

    def calculateTotalBudget(chromo):
        genes = chromo.Genes[:]
        tempSum = 0
        for gene in genes:
            tempSum += gene.allocatedBudgetValue
        return tempSum



def displayResult(lastGeneration):
    result = ""
    maxChromosome = lastGeneration[0]
    for chromosome in lastGeneration:
        if chromosome.fitness > maxChromosome.fitness:
            maxChromosome = chromosome

    result += "The final marketing budget allocation is :\n"
    for gene in maxChromosome.Genes:
        result += gene.channelName + " -> " + str(gene.allocatedBudgetValue) + "K\n"
    result += "The total profit is " + str(maxChromosome.fitness) + "K\n"
    result += "**********************************************\n"
    return result



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


    # print("First Generation : ")
    # for chromosome in chromosmeList1:
        # chromosome.showChromosome()
        # print('*******************************')
    f = open("the Output File.txt", "w")
    n = 0
    isUniform = True
    sizeOfGeneration = 500
    finalResult = []
    for j in range(2):

        if j == 1:
            isUniform = False
            f.write("Using Non-uniform Mutution  ****************************************\n")
        else:
            f.write("Using Uniform Mutution  ****************************************\n")
        for i in range(20):
            chromosmeList1 = []
            for k in range(5):
                Genes = Representation(ROIDictionary, boundariesList, totalBudget)
                ch1 = Chromosome(Genes, numberOfChannels, totalBudget)
                chromosmeList1.append(ch1)
            print("itretion " , i)
            while n < sizeOfGeneration:
                ga = GeneticA(0.5 , 0.3)
                chromosmeList2 = ga.CreateNewGeneration(chromosmeList1 , isUniform , n , sizeOfGeneration)
                chromosmeList1 = copy.deepcopy(chromosmeList2)
                n += 1
            n = 0
            result = displayResult(chromosmeList2)
            f.write(result)
            print(result)

    f.close()

