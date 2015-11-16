__author__ = 'rsimpson'


from geneticAlgorithm import *


class BlueGene(Gene):
    def __init__(self):
        # call the parent constructor
        Gene.__init__(self)
        # choose a random value to start
        self.randomInit()

    def randomInit(self):
        # 65 is ASCII capital A, choose a value between A and Z
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
        # start with a fitness of zero
        fitness = 0
        # define what the goal string is
        goal = 'HELLOWORLD'
        # for each gene in the chromosome...
        for i in range(0, len(goal)):
            # increase fitness by the square of the 'distance' of the gene's value (a letter from A to Z) from the goal value
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


geneticAlgorithm(BluePopulation(20, 10))