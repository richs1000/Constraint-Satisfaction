__author__ = 'rsimpson'

import random
from geneticAlgorithm import *

class MapColoringGene(Gene):
    '''
    Each gene represents a state (e.g., Northern Territories). The value of each state is the color chosen for that
    state.
    '''
    def __init__(self, _name):
        # call the parent constructor
        Gene.__init__(self)
        # choose a random value to start
        self.randomInit()
        # keep track of which state in Australia this gene represents
        self.name = _name

    def printGene(self):
        print "name = " + self.name + "\tvalue = " + str(self.value)

    def randomInit(self):
        global GRIDSIZE
        # choose a value for the gene - states can be colored red, blue or green
        self.value = random.choice(['red', 'green', 'blue'])


class MapColoringChromosome(Chromosome):
    '''
    A chromosome is a color assignment for each state. The chromosome stores a list of gene objects in
    self.genes
    '''
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
        # create a list of state names
        states = ['NSW', 'V', 'T', 'WA', 'NT', 'SA', 'Q']
        # for each position in the chromosome (i.e., each state in Australia)...
        for state in range(0, self.length):
            # create a new gene
            newGene = MapColoringGene(states[state])
            # add the gene to the chromosome
            self.genes.append(newGene)

    def fitnessFunction(self):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        # start accumulator at zero
        fitness = 0
        # create a list of gene pairs within the chromosome that cannot be equal
        # each pair contains an index for two genes within the chromosome (a list of genes)
        constraintList = [(3, 4), (3, 5), (6, 4), (5, 4), (5, 6), (5, 0), (5, 1), (0, 1), (6, 0)]
        # check whether the queen represented by this gene
        for constraint in constraintList:
            # get index of genes within chromosome
            geneIndex1 = constraint[0]
            geneIndex2 = constraint[1]
            # get value of each gene
            gene1 = self.genes[geneIndex1]
            gene2 = self.genes[geneIndex2]
            # if the genes are equal then add 1 to our fitness score
            if gene1.value == gene2.value:
                fitness += 1
        # return the total fitness
        return fitness


class MapColoringPopulation(Population):
    def __init__(self, populationSize, chromosomeSize):
        # call the parent constructor
        Population.__init__(self, populationSize)
        # create a random population
        self.randomPopulation(chromosomeSize)

    def randomPopulation(self, chromosomeSize):
        for i in range(0, self.populationSize):
            self.generation.put(MapColoringChromosome(chromosomeSize))


geneticAlgorithm(MapColoringPopulation(10, 7))