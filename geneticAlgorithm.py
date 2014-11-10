__author__ = 'rsimpson'


import random
import copy
from Queue import PriorityQueue


class Population:
    def __init__(self, populationSize):
        """
        Create a class that holds the collection of chromosomes (the 'population')
        """
        # a generation is a collection of chromosomes stored in a priority queue
        # which is ordered by fitness
        self.generation = PriorityQueue()
        # how many chromosomes in each generation?
        self.populationSize = populationSize
        # create a random population
        self.randomPopulation()

    def randomPopulation(self):
        for i in range(0, self.populationSize):
            self.generation.put(Chromosome())

    def selection(self):
        """
        Decide which members of the population survive to the next generation
        """
        # calculate fitness scores and survival probabilities
        self.calculateFitness()
        # create an empty priority queue for the new generation
        newGeneration = PriorityQueue()
        # pick top half of the population to survive
        for c in range(0, self.populationSize / 2):
            # get a chromosome
            chromosome = self.generation.get()
            # put the chromosomes in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration


    def crossOver(self):
        """
        Fill in the rest of the population by 'mating' pairs of chromosomes
        """
        # calculate fitness scores and survival probabilities
        self.calculateFitness()
        # create an empty priority queue for the new generation
        newGeneration = PriorityQueue()
        # keep going until we've got a full population
        while self.generation.qsize() + newGeneration.qsize() < self.populationSize:
            # get a chromosome
            chromosome1 = self.generation.get()
            # get a second chromosome
            if not self.generation.empty():
                chromosome2 = self.generation.get()
            else:
                break
            # copy the chromosome
            copy1 = copy.deepcopy(chromosome1)
            copy2 = copy.deepcopy(chromosome2)
            # mutate the copies
            copy1.crossOver(copy2)
            # put the chromosomes in the new generation
            newGeneration.put(chromosome1)
            newGeneration.put(chromosome2)
            newGeneration.put(copy1)
            newGeneration.put(copy2)
        # keep the new generation
        while not newGeneration.empty():
            chromosome = newGeneration.get()
            self.generation.put(chromosome)

    def mutate(self, mutationProbability):
        # calculate fitness scores and survival probabilities
        self.calculateFitness()
        # create an empty priority queue for the new generation
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # mutate the chromosome
            chromosome.mutate(mutationProbability)
            # put the chromosome in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration

    def calculateFitness(self):
        # create an empty priority queue to hold chromosomes
        newGeneration = PriorityQueue()
        # add up all the fitness scores
        totalFitness = 0
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # calculate the fitness score
            chromosome.fitness = chromosome.fitnessFunction('HELLOWORLD')
            # add the fitness score to the running total
            totalFitness += chromosome.fitness
            # put the chromosome in the new priority queue
            newGeneration.put(chromosome)
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not newGeneration.empty():
            # get another chromosome
            chromosome = newGeneration.get()
            # calculate the survival probability
            chromosome.survivalProbability = float(chromosome.fitness) / totalFitness
            # put the chromosome in the new priority queue
            self.generation.put(chromosome)

    def foundAWinner(self,goal):
        # create an empty priority queue
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # see if this matches
            if chromosome.fitnessFunction(goal) == 0:
                return (True, chromosome)
            # put the chromosome in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration
        # report that we haven't found a winner yet
        return (False, 'nuts')

    def printPopulation(self):
        # create an empty priority queue
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and print each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # see if this matches
            chromosome.printChromosome()
            # put the chromosome in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration


class Chromosome:
    def __init__(self):
        """
        Each chromosome represents a single potential solution
        """
        # each chromosome is a collection of individual 'genes' that make up
        # the solution
        self.value = []
        # how many 'genes' in each chromosome?
        self.length = 10
        # choose random values for the chromosome
        self.randomInit()
        # initialize fitness score
        self.fitness = self.fitnessFunction('HELLOWORLD')
        # survival probability
        self.survivalProbability = 0

    def printChromosome(self):
        print "value = " + str(self.value)
        print "fitness = " + str(self.fitness)

    def __cmp__(self, other):
        """
        Compare two chromosomes based on fitness
        :param other:
        :return:
        """
        return cmp(self.fitness, other.fitness)

    def randomInit(self):
        """
        choose random values for the chromosome
        """
        for index in range(0, self.length):
            self.value.append(chr(random.randint(0, 25) + 65))

    def fitnessFunction(self, goal):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        fitness = 0
        for i in range(0, len(goal)):
            fitness += (ord(self.value[i]) - ord(goal[i])) * (ord(self.value[i]) - ord(goal[i]))
        return fitness

    def crossOver(self, other):
        """
        Given the indices of two chromosomes, 'mate' them and return two new
        chromosomes
        """
        # find the mid-point
        pivot = random.randint(0, len(self.value))
        # swap the values around the mid-point
        newChrom1 = self.value[0:pivot] + other.value[pivot:other.length]
        newChrom2 = other.value[0:pivot] + self.value[pivot:self.length]
        # replace the old chromosomes with the mutated pair
        self.value = newChrom1
        other.value = newChrom2

    def mutate(self, mutationProbability):
        # roll the dice - are we going to mutate?
        if (random.random() > mutationProbability):
            return
        # choose a random gene
        gene = random.randint(0, len(self.value)-1)
        # choose whether to add or subtract
        multiplier = 1
        if random.randint(0, 1) == 1:
            multiplier = -1
        # mutate the gene by adding or subtracting one
        newValue = ord(self.value[gene])
        newValue += multiplier * 1
        # store new gene value
        self.value[gene] = chr(newValue)

def geneticAlgorithm():
    # create an initial population
    pop = Population(20)
    loopCount = 0
    # keep looping until we find a solution or we exceed our loop limit
    while (loopCount < 10000):
        winnerTuple = pop.foundAWinner('HELLOWORLD')
        if (winnerTuple[0]):
            print "done!"
            pop.printPopulation()
            return winnerTuple[1]
        # selection
        pop.selection()
        # crossover
        pop.crossOver()
        # mutation
        pop.mutate(.07)
        # increment loop count
        loopCount += 1
        if (loopCount % 100 == 0):
            print "loop count = " + str(loopCount)
            pop.printPopulation()

geneticAlgorithm()