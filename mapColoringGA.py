__author__ = 'rsimpson'

import random
from geneticAlgorithm import *


# The number of chromosomes in each generation
POPULATION_SIZE = 10



class MapColoringGene(Gene):
    '''
    Each gene represents a state. The value for each gene is the color of the state.
    '''
    def __init__(self, _strName):
        # call the parent constructor
        Gene.__init__(self, _strName, ['red', 'green', 'blue'])


class MapColoringChromosome(Chromosome):
    '''
    A chromosome is a location assignment for each building. The chromosome stores a list of gene objects in
    self.genes
    '''
    def __init__(self):
        # create a gene object for each state in the map
        # start with an empty list for the genes...
        lstGenes = []
        # and a list of state names
        states = ['NSW', 'V', 'T', 'WA', 'NT', 'SA', 'Q']
        # for each state name...
        for state in states:
            # create a new gene object and add it to the list of genes
            lstGenes.append(MapColoringGene(state))
        # call the parent constructor with a list of gene objects
        Chromosome.__init__(self, lstGenes)

    def fitness(self):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        # start accumulator at zero
        fitness = 0
        # create a list of gene pairs within the chromosome that cannot be equal
        # each pair contains the names for two genes within the chromosome (a list of genes)
        constraintList = [('WA', 'NT'), ('WA', 'SA'), ('Q', 'NT'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('NSW', 'V'), ('Q', 'NSW')]
        # loop through each pair of genes in the chromosome, starting with the first gene...
        for g1 in range(0, len(self.genes)-1):
            # and comparing it to every gene that follows
            for g2 in range(g1+1, len(self.genes)):
                # loop through each constraint pair
                for constraint in constraintList:
                    # get pointers to the two genes being compared
                    gene1 = self.genes[g1]
                    gene2 = self.genes[g2]
                    # check gene values against the constraint - if the names match the constraint
                    if (((gene1.name == constraint[0] and gene2.name == constraint[1]) \
                        or (gene1.name == constraint[1] and gene2.name == constraint[0])) \
                        # and the genes have the same value
                        and (gene1.value == gene2.value)):
                        # increase the fitness value
                        fitness += 1
        # return the total fitness
        return fitness


class MapColoringPopulation(Population):
    def __init__(self, _populationSize, _chromosomeClass):
        # call the parent constructor and pass it a chromosome object to use as a template
        Population.__init__(self, _populationSize, _chromosomeClass)


geneticAlgorithm(MapColoringPopulation(POPULATION_SIZE, MapColoringChromosome))
