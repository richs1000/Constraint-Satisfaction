__author__ = 'rsimpson'


import random
import copy
from Queue import PriorityQueue


class Gene:
    def __init__(self):
        self.value = None

    def printGene(self):
        print "value = " + str(self.value)

    def randomInit(self):
        pass


class Chromosome:
    def __init__(self, length):
        """
        Each chromosome represents a single potential solution
        """
        # each chromosome is a collection of individual 'genes' that make up
        # the solution
        self.genes = []
        # how many 'genes' in each chromosome?
        self.length = length
        # initialize fitness score
        self.fitness = 0

    def printChromosome(self):
        for gene in self.genes:
            gene.printGene()
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
        pass

    def fitnessFunction(self, goal):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        pass

    def crossOver(self, other):
        """
        Given the indices of two chromosomes, 'mate' them and return two new
        chromosomes
        """
        # find the mid-point
        pivot1 = random.randint(0, len(self.genes))
        pivot2 = random.randint(0, len(self.genes))
        # swap the values around the mid-point
        newChrom1 = self.genes[0:pivot1] + other.genes[pivot1:other.length]
        newChrom2 = other.genes[0:pivot2] + self.genes[pivot2:self.length]
        # replace the old chromosomes with the mutated pair
        self.genes = newChrom1
        other.value = newChrom2

    def mutate(self, mutationProbability):
        # roll the dice - are we going to mutate?
        if (random.random() > mutationProbability):
            return
        # choose a random gene
        geneIndex = random.randint(0, len(self.genes)-1)
        gene = self.genes[geneIndex]
        # mutate the gene by choosing a random value
        gene.randomInit()


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

    def randomPopulation(self, chromosomeSize):
        pass

    def selection(self):
        """
        Decide which members of the population survive to the next generation
        """
        # calculate fitness scores
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
        # calculate fitness scores
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
        # calculate fitness scores
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
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # calculate the fitness score
            chromosome.fitness = chromosome.fitnessFunction()
            # put the chromosome in the new priority queue
            newGeneration.put(chromosome)
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not newGeneration.empty():
            # get another chromosome
            chromosome = newGeneration.get()
            # put the chromosome in the new priority queue
            self.generation.put(chromosome)

    def foundAWinner(self):
        foundWinner = False
        # calculate fitness scores
        self.calculateFitness()
        # create an empty priority queue
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # see if this matches
            if chromosome.fitnessFunction() == 0:
                foundWinner = True
            # put the chromosome in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration
        # report whether we found a winner
        return foundWinner

    def printPopulation(self):
        # calculate fitness scores and survival probabilities
        self.calculateFitness()
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


class BlueGene(Gene):
    def __init__(self):
        # call the parent constructor
        Gene.__init__(self)
        # choose a random value to start
        self.randomInit()

    def randomInit(self):
        self.value = chr(random.randint(0, 25) + 65)


class BlueChromosome(Chromosome):
    def __init__(self, length):
        # call the parent constructor
        Chromosome.__init__(self, length)
        # choose random values for the chromosome
        self.randomInit()
        # initialize fitness score
        self.fitness = self.fitnessFunction()

    def randomInit(self):
        """
        choose random values for the chromosome
        """
        for index in range(0, self.length):
            # create a new gene
            newGene = BlueGene()
            # add the gene to the chromosome
            self.genes.append(newGene)

    def fitnessFunction(self):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        fitness = 0
        goal = 'HELLOWORLD'
        for i in range(0, len(goal)):
            fitness += (ord(self.genes[i].value) - ord(goal[i])) * (ord(self.genes[i].value) - ord(goal[i]))
        return fitness


class BluePopulation(Population):
    def __init__(self, populationSize, chromosomeSize):
        # call the parent constructor
        Population.__init__(self, populationSize)
        # create a random population
        self.randomPopulation(chromosomeSize)

    def randomPopulation(self, chromosomeSize):
        for i in range(0, self.populationSize):
            self.generation.put(BlueChromosome(chromosomeSize))


def geneticAlgorithm(population):
    loopCount = 0
    # keep looping until we find a solution or we exceed our loop limit
    while (loopCount < 10000):
        if (population.foundAWinner()):
            print "found a winner"
            population.printPopulation()
            return
        # selection
        population.selection()
        # crossover
        population.crossOver()
        # mutation
        population.mutate(.07)
        # increment loop count
        loopCount += 1
        if (loopCount % 100 == 0):
            print "loop count = " + str(loopCount)

#geneticAlgorithm(BluePopulation(20, 10))