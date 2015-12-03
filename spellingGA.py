__author__ = 'rsimpson'


from geneticAlgorithm import *


# The number of chromosomes in each generation
POPULATION_SIZE = 10


class BlueGene(Gene):
    '''
    Each gene represents a state. The value for each gene is the color of the state.
    '''
    def __init__(self, _strName):
        # the domain is all the capital letters
        lstDomain = [chr(c + 65) for c in range(26)]
        # call the parent constructor
        Gene.__init__(self, _strName, lstDomain)


class BlueChromosome(Chromosome):
    '''
    A chromosome is an assignment for each character in the string. The chromosome stores a list of gene objects in
    self.genes
    '''
    def __init__(self, _length=10):
        # create a gene object for each state in the map
        # start with an empty list for the genes...
        lstGenes = []
        # for each character in the string...
        for character in range(0, _length):
            # create a new gene object and add it to the list of genes
            lstGenes.append(BlueGene(str(character)))
        # call the parent constructor with a list of gene objects
        Chromosome.__init__(self, lstGenes)

    def fitness(self):
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

    def crossOver(self, _other):
        """
        Given two chromosomes, 'mate' them and return two new chromosomes
        This implements a two-point cross-over
        """
        # choose two points
        pivot1 = random.randint(1, len(self.genes)/2)
        pivot2 = random.randint(len(self.genes)/2 + 1, len(self.genes)-1)
        # swap the values around the mid-point
        newChrom1 = self.genes[0:pivot1] + _other.genes[pivot1:pivot2] + self.genes[pivot2:len(self.genes)]
        newChrom2 = _other.genes[0:pivot1] + self.genes[pivot1:pivot2] + _other.genes[pivot2:len(self.genes)]
        # return a tuple with the two new chromosomes
        return (newChrom1, newChrom2)


class MapColoringPopulation(Population):
    def __init__(self, _populationSize, _chromosomeClass):
        # call the parent constructor and pass it a chromosome object to use as a template
        Population.__init__(self, _populationSize, _chromosomeClass)


geneticAlgorithm(MapColoringPopulation(POPULATION_SIZE, BlueChromosome), .05)
