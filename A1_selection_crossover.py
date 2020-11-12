import random

def crossover(chromosome1,chromosome2,rc):
  r = random.uniform(0, 1)
  r = round(r, 1)
  
  if r < rc or r == rc :
      randomIndex = random.randint(1, len(chromosome1) - 1)
      print(randomIndex)
      offspring1 = chromosome1[0:randomIndex] + chromosome2[randomIndex:]
      offspring2 = chromosome2[0:randomIndex] + chromosome1[randomIndex:]
      return offspring1, offspring2
  else:
      print(r)
      return chromosome1,chromosome2
      
      
      
def Selection(chromosome1, chromosome2):
    return calculate_fitness(chromosome1) > calculate_fitness(chromosome2) ? chromosome1: chromosome2
    
    
print (crossover([1,0,1,1], [0,0,0,1], 0.8))




