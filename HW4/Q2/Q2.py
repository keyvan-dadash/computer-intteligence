import random
import numpy as np


MUTATION_PERCENT = 60
MUTATION_REPEAT = 2
WORST_THRE = 850


class Genome:
    chromosomes = []
    fitness = 9999
    
    
    def __init__(self, func):
        self.func = func
        
    
    @staticmethod
    def create_population(amount, func):
        pop_list = []
        for _ in range(amount):
            newGenome = Genome(func)
            newGenome.chromosomes = random.sample( #sampling randome
                range(
                    -100, 
                    100
                ), 98)
            # newGenome.chromosomes.insert(0, 0)
            # newGenome.chromosomes.append(0)
            newGenome.fitness = newGenome.eval_fitness() #set fitness
            pop_list.append(newGenome)
        return pop_list
    
    def eval_fitness(self):
        minFit = 999999
        for i in range(len(self.chromosomes)): #calculate fitness based on distance
            if (abs(self.func(self.chromosomes[i])) < abs(minFit)):
                minFit = abs(self.func(self.chromosomes[i]))
        minFit = np.round(minFit, 5)
        return abs(minFit)
    
    @staticmethod
    def return_best_match(pop_list):
        allFitness = [i.fitness for i in pop_list]
        bestFitness = min(allFitness) #minimum distance as best fit
        return pop_list[allFitness.index(bestFitness)]
    
    @staticmethod
    def select_k_best(pop_list, k): #select best among k item from pop_lis
        selected = [pop_list[random.randrange(0, len(pop_list))] for _ in range(k)]
        bestGenome = Genome.return_best_match(selected)
        return bestGenome
    
    @staticmethod
    def cross_over(population, func):
        parent1 = Genome.select_k_best(population, 6).chromosomes
        parent2 = Genome.select_k_best(population, 6).chromosomes
        
        while True:
            if parent1 == parent2: #we should pick two diffrent parent
                parent1 = Genome.select_k_best(population, 6).chromosomes
                parent2 = Genome.select_k_best(population, 6).chromosomes
            else:
                break
            
        # if random.randrange(0, 100) < MUTATION_PERCENT:
        #     child = Genome.mutation(child)
        newGenome = Genome(func)
        # print(np.mean( np.array([ parent1, parent2 ]), axis=0 ).tolist())
        newGenome.chromosomes = np.mean( np.array([ parent1, parent2 ]), axis=0 ).tolist()
        newGenome.fitness = newGenome.eval_fitness()
        return newGenome
    
    @staticmethod
    def mutation(chromosomes):
        for _ in range(MUTATION_REPEAT):
            p1, p2 = [random.randrange(1, len(chromosomes) - 1) for i in range(2)]
            while p1 == p2:
                p2 = random.randrange(1, len(chromosomes) - 1)
            can = chromosomes[p1]
            chromosomes[p1] = chromosomes[p2]
            chromosomes[p2] = can
        return chromosomes


def func(x):
    return (9 * x ** 5) - (194.7 * x ** 4) + (1680.1 * x ** 3) - (7227.94 * x ** 2) + (15501.2 * x) - 13257.2
            
popSize=100 
maxGeneration=300
allBestFitness = []
population =  Genome.create_population(popSize, func)
generation = 0

# print(func(4.884070251137018))

# print(population)

# for _ in range(maxGeneration):
    
#     population.append(Genome.cross_over(
#             population, func
#         ))
    
#     for genom in population:
#         if genom.fitness > WORST_THRE: #remove worst gens
#             population.remove(genom)
    
#     # pop = Genome.mutation(
#     #     Genome.cross_over(
#     #         population, func
#     #     ).chromosomes
#     # )
    
#     print(population)

# print(population[0].chromosomes)

generation = 0
while generation < maxGeneration:
    generation += 1
    for i in range(int(popSize / 2)):
        population.append(Genome.cross_over(population, func)) #cross over

    for genom in population:
        if genom.fitness > WORST_THRE: #remove worst gens
            population.remove(genom)

    averageFitness = round(np.sum([genom.fitness for genom in population]) / len(population), 5)
    bestGenome = Genome.return_best_match(population)
    allBestFitness.append(bestGenome.fitness)
    
# print(bestGenome.fitness)
min = 999999999999999
index = -300
for i in bestGenome.chromosomes:
    if abs(func(i)) < abs(min):
        index = i
        min = abs(func(i))
        
print(index)
