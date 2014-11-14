__author__ = 'rsimpson'
"""
    cspGraph.addFeature('NSW', ['red', 'green', 'blue'])
    cspGraph.addFeature('V', ['red', 'green', 'blue'])
    cspGraph.addFeature('T', ['red', 'green', 'blue'])
    cspGraph.addFeature('WA', ['red', 'green', 'blue'])
    cspGraph.addFeature('NT', ['red', 'green', 'blue'])
    cspGraph.addFeature('SA', ['red', 'green', 'blue'])
    cspGraph.addFeature('Q', ['red', 'green', 'blue'])
    constraintList = [('WA', 'NT'), ('WA', 'SA'), ('Q', 'NT'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('NSW', 'V'), ('Q', 'NSW')]
"""

import random
from geneticAlgorithm import *

class MapColoringGene(Gene):
    def __init__(self):
        # call the parent constructor
        Gene.__init__(self)
        # choose a random value to start
        self.randomInit()

    def randomInit(self):
        global GRIDSIZE
        colors = ['red', 'green', 'blue']
        index = random.randint(0, len(colors)-1)
        # choose a value
        self.value = colors[index]


class MapColoringChromosome(Chromosome):
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
        for row in range(0, self.length):
            # create a new gene
            newGene = MapColoringGene()
            # add the gene to the chromosome
            self.genes.append(newGene)

    def fitnessFunction(self):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        # start accumulator at zero
        fitness = 0
        constraintList = [(3, 4), (3, 5), (6, 4), (5, 4), (5, 6), (5, 0), (5, 1), (0, 1), (6, 0)]
        # check whether the queen represented by this gene
        for constraint in constraintList:
            geneIndex1 = constraint[0]
            geneIndex2 = constraint[1]
            gene1 = self.genes[geneIndex1]
            gene2 = self.genes[geneIndex2]
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