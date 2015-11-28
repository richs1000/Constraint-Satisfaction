__author__ = 'rsimpson'

import random
from geneticAlgorithm import *


# The number of chromosomes in each generation
POPULATION_SIZE = 10

class AdminBldgGene(Gene):
    '''
    Each gene represents a building. The value for each gene is the position on the campus grid where the building
    is located.
    '''
    def __init__(self):
        # call the parent constructor
        Gene.__init__(self, 'Administration', [1, 3, 5, 6])


class BusStopGene(Gene):
    '''
    Each gene represents a building. The value for each gene is the position on the campus grid where the building
    is located.
    '''
    def __init__(self):
        # call the parent constructor
        Gene.__init__(self, 'Bus Stop', [3, 6])


class ClassroomGene(Gene):
    '''
    Each gene represents a building. The value for each gene is the position on the campus grid where the building
    is located.
    '''
    def __init__(self):
        # call the parent constructor
        Gene.__init__(self, 'Classroom', [1, 2, 3, 4, 5, 6])


class DormitoryGene(Gene):
    '''
    Each gene represents a building. The value for each gene is the position on the campus grid where the building
    is located.
    '''
    def __init__(self):
        # call the parent constructor
        Gene.__init__(self, 'Dormitory', [2, 3, 4, 6])


class CampusLayoutChromosome(Chromosome):
    '''
    A chromosome is a location assignment for each building. The chromosome stores a list of gene objects in
    self.genes
    '''
    def __init__(self):
        # call the parent constructor with a list of gene objects
        Chromosome.__init__(self, [AdminBldgGene(), BusStopGene(), ClassroomGene(), DormitoryGene()])

    def adjacent(self, tailValue, headValue):
        """
        returns true if constraint is satisfied and false if it is not
        """
        if (tailValue == 1 and (headValue == 2 or headValue == 4)):
            return True
        elif ((tailValue == 2) and (headValue == 1 or headValue == 3 or headValue == 5)):
            return True
        elif ((tailValue == 3) and (headValue == 2 or headValue == 6)):
            return True
        elif ((tailValue == 4) and (headValue == 1 or headValue == 5)):
            return True
        elif ((tailValue == 5) and (headValue == 2 or headValue == 4 or headValue == 6)):
            return True
        elif ((tailValue == 6) and (headValue == 3 or headValue == 5)):
            return True
        # otherwise, constraint is not satisfied so return false
        return False

    def fitness(self):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        # start accumulator at zero
        fit = 0
        # create a list of gene pairs within the chromosome representing buidlings that CANNOT be adjacent
        # each pair contains an index for two genes within the chromosome (a list of genes)
        # Administration building (A) must NOT be adjacent to the dormitory (D)
        notAdjacentList = [(0, 3), (3, 0)]
        # create a list of gene pairs within the chromosome representing buildings that MUST be adjacent
        # Administration building (A) must be adjacent to the bus stop (B)
        # Classroom (C) must be adjacent to the bus stop (B)
        # Classroom (C) must be adjacent to the dormitory (D)
        adjacentList = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)]
        # create a list of illegal values for genes
        notEqualList = [(0, 2), (0, 4), (1, 1), (1, 2), (1, 4), (1, 5), (3, 1), (3, 5)]
        # genes cannot have the same value
        for gene1 in range(0, len(self.genes)-1):
            for gene2 in range(gene1+1, len(self.genes)):
                if self.genes[gene1].value == self.genes[gene2].value:
                    fit += 1
        # check each gene against list of illegal values
        for constraint in notEqualList:
            # get index of gene within chromosome
            geneIndex = constraint[0]
            # get illegal value
            illegalValue = constraint[1]
            # get value of each gene
            geneValue = self.genes[geneIndex].value
            # if the genes are not adjacent then add 1 to our fitness score
            if geneValue == illegalValue:
                fit += 1
        # check each gene against the adjacency constraints
        for constraint in adjacentList:
            # get index of genes within chromosome
            geneIndex1 = constraint[0]
            geneIndex2 = constraint[1]
            # get value of each gene
            gene1 = self.genes[geneIndex1]
            gene2 = self.genes[geneIndex2]
            # if the genes are not adjacent then add 1 to our fitness score
            if not self.adjacent(gene1.value, gene2.value):
                fit += 1
        # check each gene against the non-adjacency constraints
        for constraint in notAdjacentList:
            # get index of genes within chromosome
            geneIndex1 = constraint[0]
            geneIndex2 = constraint[1]
            # get value of each gene
            gene1 = self.genes[geneIndex1]
            gene2 = self.genes[geneIndex2]
            # if the genes are adjacent then add 1 to our fitness score
            if self.adjacent(gene1.value, gene2.value):
                fit += 1
        # return the total fitness
        return fit


class CampusLayoutPopulation(Population):
    def __init__(self, _populationSize, _chromosomeClass):
        # call the parent constructor and pass it a chromosome object to use as a template
        Population.__init__(self, _populationSize, _chromosomeClass)

geneticAlgorithm(CampusLayoutPopulation(POPULATION_SIZE, CampusLayoutChromosome))