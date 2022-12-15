import math
import random
import numpy as np
import matplotlib.pyplot as plt


MUTATION_PERCENT = 60
MUTATION_REPEAT = 2
WORST_THRE = 850

points_location = [[2, 7], [4, 19], [17, 15], [20, 28], [18, 29], [20, 14], [30, 42], [23, 33], [12, 42], [33, 36], [42, 45]]

number_of_points = len(points_location)

def cal_dist(a, b):
    dis = math.sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))
    return np.round(dis, 2)


class Genome:
    chromosomes = []
    fitness = 9999

    @staticmethod
    def create_population(amount):
        pop_list = []
        for _ in range(amount):
            newGenome = Genome()
            newGenome.chromosomes = random.sample( #sampling randome
                range(
                    1, 
                    number_of_points
                ), number_of_points - 1)
            newGenome.chromosomes.insert(0, 0)
            newGenome.chromosomes.append(0)
            newGenome.fitness = newGenome.eval_fitness() #set fitness
            pop_list.append(newGenome)
        return pop_list

    def eval_fitness(self):
        calculatedFitness = 0
        for i in range(len(self.chromosomes) - 1): #calculate fitness based on distance
            p1 = points_location[self.chromosomes[i]]
            p2 = points_location[self.chromosomes[i + 1]]
            calculatedFitness += cal_dist(p1, p2)
        calculatedFitness = np.round(calculatedFitness, 5)
        return calculatedFitness


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
    def cross_over(population):
        parent1 = Genome.select_k_best(population, 12).chromosomes
        parent2 = Genome.select_k_best(population, 6).chromosomes
        
        while True:
            if parent1 == parent2: #we should pick two diffrent parent
                parent1 = Genome.select_k_best(population, 12).chromosomes
                parent2 = Genome.select_k_best(population, 6).chromosomes
            else:
                break


        size = len(parent1)
        child = [-1] * size
        child[0], child[size - 1] = 0, 0
        point = random.randrange(5, size - 4)
        for i in range(point, point + 4):
            child[i] = parent1[i]
        point += 4
        point2 = point
        while child[point] in [-1, 0]:
            if child[point] == 0:
                point += 1
                if point == size:
                    point = 0
            else:
                if parent2[point2] not in child:
                    child[point] = parent2[point2]
                    point += 1
                    if point == size:
                        point = 0
                else:
                    point2 += 1
                    if point2 == size:
                        point2 = 0

        if random.randrange(0, 100) < MUTATION_PERCENT: #shall?
            child = Genome.mutation(child)
            
        newGenome = Genome()
        newGenome.chromosomes = child
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


if __name__ == "__main__":
    popSize=100 
    maxGeneration=300
    allBestFitness = []
    population =  Genome.create_population(popSize)
    generation = 0
    while generation < maxGeneration:
        generation += 1
        for i in range(int(popSize / 2)):
            population.append(Genome.cross_over(population)) #cross over

        for genom in population:
            if genom.fitness > WORST_THRE: #remove worst gens
                population.remove(genom)

        averageFitness = round(np.sum([genom.fitness for genom in population]) / len(population), 5)
        bestGenome = Genome.return_best_match(population)
        allBestFitness.append(bestGenome.fitness)
        
    print(bestGenome.fitness)

    start = None
    for x, y in points_location:
        if start is None:
            start = points_location[0]
            plt.scatter(start[0], start[1], c="green", marker=">")
            plt.annotate("Start", (x + 2, y - 4))
        else:
            plt.scatter(x, y, c="black")

    xx = [points_location[i][0] for i in bestGenome.chromosomes]
    yy = [points_location[i][1] for i in bestGenome.chromosomes]

    for x, y in zip(xx, yy):
        plt.text(x + 1, y - 1, str(yy.index(y)), color="green", fontsize=10)

    plt.plot(xx, yy, color="blue", linewidth=1, linestyle="-")
    plt.show()