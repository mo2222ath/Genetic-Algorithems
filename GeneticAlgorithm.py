import random
import A1

class GA:
    finalResult = 0
    generation = []
    probOfCross = 0.0
    probOfMutate = 0.0
    


    def __init__(generation , probOfCross , probOfMutate):
        self.generation = generation
        self.probOfCross = probOfCross
        self.probOfMutate = probOfMutate
        
        
        


    
    def CreateGeneration():
        n1 = random.randint(0,len(generation))
        n2 = random.randint(0,len(generation))
        frist = self.Selection(generation[n1],generation[n2])
        n3 = random.randint(0,len(generation))
        n4 = random.randint(0,len(generation))
        second = self.Selection(generation[n3],generation[n4])
        offSpring1 , offSpring2 = crossover(frist,second ,probOfCross)
        offSpring1 , offSpring2 = mutate(offSpring1,offSpring2,probOfMutate)
        isFeasible =  checkConstraints(offSpring1 , generation[0].numberOfInstanceWeapons, generation[0].numberOfTargets )
        if !isFeasible: offSpring1 = fixChromosome(offSpring1)
        isFeasible =  checkConstraints(offSpring2 , generation[0].numberOfInstanceWeapons, generation[0].numberOfTargets )
        if !isFeasible: offSpring2 = fixChromosome(offSpring2)
        
        # if generation[n1].fitness > offSpring1.


    def Selection(chromosome1, chromosome2):
        return chromosome1 if chromosome1.fitness < chromosome2.fitness else chromosome2

    def crossover(chromosome1, chromosome2, rc):
        r = random.uniform(0, 1)
        r = round(r, 1)
        if r <= rc:
            randomIndex = random.randint(1, len(chromosome1.Genes) - 1)
            # print(randomIndex)
            genesOffspring1 = chromosome1.Genes[0:randomIndex] + chromosome2.Genes[randomIndex:]
            genesOffspring2 = chromosome2.Genes[0:randomIndex] + chromosome1.Genes[randomIndex:]
            offSpring1 = Chromosome(genesOffspring1 , chromosome1.numberOfTargets,chromosome1.numberOfTypeWeapons,chromosome1.damagingTarget,chromosome1.threatCoefficient)
            offSpring2 = Chromosome(genesOffspring2 , chromosome1.numberOfTargets,chromosome1.numberOfTypeWeapons,chromosome1.damagingTarget,chromosome1.threatCoefficient)
            return offspring1, offspring2
        else:
            return chromosome1, chromosome2




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
                    # print("Chromosome is not feasible")
                    feasible = False
                    return feasible
                else:
                    arrNum = arrNum + 1
            if not feasible:
                return feasible
            counter2 = counter2 + 1

    def fixChromosome(chromosome):
        for i in range(self.numberOfTargets):
            for j in range(self.numberOfInstanceWeapons):
                if i==0:
                   temp = chromosome[:5]
                else:
                    if temp[j] == 1:
                        temp[j] = 2
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


















