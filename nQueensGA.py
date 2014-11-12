__author__ = 'rsimpson'

import random
from geneticAlgorithm import *

# This value is used to determine the size of the board when doing an n-queens problem
GRIDSIZE = 5

# This is a list of lists - where each sub-list contains the indices that are in the
# same column.
NQUEENS_COLUMNS = []

# This is a list of lists - where each sub-list contains the indices that are in the
# same diagonal.
NQUEENS_DIAGONALS = []


def createNQueensGlobals():
    # get access to global variables
    global GRIDSIZE
    global NQUEENS_COLUMNS
    global NQUEENS_DIAGONALS
    # each list within this list will contain all the indexes for
    # a single column of the board
    NQUEENS_COLUMNS = []
    # loop through all the columns in the board
    for col in range(0, GRIDSIZE):
        # each column has gridSize elements, each separated by gridSize items
        NQUEENS_COLUMNS.append(range(col, GRIDSIZE*GRIDSIZE, GRIDSIZE))
    # each list within this list contains all the indexes for
    # a single diagonal on the board
    NQUEENS_DIAGONALS = []
    for index in range(0, GRIDSIZE):
        # diagonals starting in upper left corner and going to middle of grid
        NQUEENS_DIAGONALS.append(range(index, index * GRIDSIZE + 1, GRIDSIZE - 1))
        # diagonals starting in upper right corner and going to lower right corner
        NQUEENS_DIAGONALS.append(range((index+1) * GRIDSIZE - 1, GRIDSIZE * GRIDSIZE - 1, GRIDSIZE - 1))
        # diagonals starting in upper left corner and going to upper right corner
        NQUEENS_DIAGONALS.append(range(index, GRIDSIZE * (GRIDSIZE - index), GRIDSIZE + 1))
        # diagonals starting in upper left corner and going to lower left corner
        NQUEENS_DIAGONALS.append(range(index * GRIDSIZE, GRIDSIZE * GRIDSIZE, GRIDSIZE + 1))


class NQueensGene(Gene):
    def __init__(self, row):
        # call the parent constructor
        Gene.__init__(self)
        # which row of the board does this gene represent?
        self.row = row
        # choose a random value to start
        self.randomInit()

    def randomInit(self):
        global GRIDSIZE
        # choose a value as an offset from the start of the row
        self.value = self.row * GRIDSIZE + random.randint(0 ,GRIDSIZE - 1)


class NQueensChromosome(Chromosome):
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
            newGene = NQueensGene(row)
            # add the gene to the chromosome
            self.genes.append(newGene)

    def countViolations(self, gene0, gene1):
        """
        returns true if constraint is satisfied and false if it is not
        """
        global NQUEENS_DIAGONALS, NQUEENS_COLUMNS
        # start accumulator at zero
        violationCount = 0
        # loop through the list of column lists
        for columnList in NQUEENS_COLUMNS:
            # if both genes are assigned and in the same column
            if ((gene0.value in columnList) and (gene1.value in columnList)):
                # then increment the violation count
                violationCount += 1
        # loop through the list of diagonal lists
        for diagonalList in NQUEENS_DIAGONALS:
            # if both features are in the same diagonal
            if ((gene0.value in diagonalList) and (gene1.value in diagonalList)):
                # then increment the violation count
                violationCount += 1
        # return the square of the number of violation counts
        # (to create more separation between fitness scores)
        return violationCount * violationCount

    def fitnessFunction(self):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        # start accumulator at zero
        fitness = 0
        # check whether the queen represented by this gene
        for gene1 in range(0, len(self.genes)-1):
            # violates any constraints with the queen represented by all the other genes
            for gene2 in range(gene1 + 1, len(self.genes)):
                # add up the number of constraint violations
                fitness += self.countViolations(self.genes[gene1], self.genes[gene2])
        # return the total fitness
        return fitness


class NQueensPopulation(Population):
    def __init__(self, populationSize, chromosomeSize):
        # initialize global variables
        createNQueensGlobals()
        # call the parent constructor
        Population.__init__(self, populationSize)
        # create a random population
        self.randomPopulation(chromosomeSize)

    def randomPopulation(self, chromosomeSize):
        for i in range(0, self.populationSize):
            self.generation.put(NQueensChromosome(chromosomeSize))


geneticAlgorithm(NQueensPopulation(50, GRIDSIZE))