__author__ = 'rsimpson'


#
# I modified my older code so that each gene gets an explicit domain
#

import random
import copy
from Queue import PriorityQueue


# This variable sets the limit for the total number of times through the genetic algorithm
# loop before we give up
LOOP_LIMIT = 10000

# This variable determines the number of loops that must occur before we print the
# current population
PRINT_FREQUENCY = 100

# This variable determines what fraction of the population is kept during selection
# 2 -> keep top half; 3 -> keep top third...
SELECTION_FRACTION = 2


class Gene(object):
    '''
    Genes represent features/variables of a solution. Each gene has a domain
    '''
    def __init__(self, _strName, _lstDomain):
        # store a name for the gene - can be as simple as a number for its position
        self.name = _strName
        # keep a list of potential values for the gene
        self.domain = _lstDomain
        # start out with a random value
        self.value = self.randomValue()

    def printGene(self, _verbose=False):
        if _verbose:
            # print the name and value of each gene on a separate line
            print "name = " + self.name + "\tvalue = " + str(self.value)
        else:
            # print the value of the gene, without a newline
            print str(self.value) + " ",

    def randomValue(self):
        # choose a value for the gene randomly. this function may be overridden
        # by the problem-specific sub-class
        # the default is to choose a random value from the gene's domain
        return random.choice(self.domain)


class Chromosome(object):
    '''
    A chromosome is a collection of genes. Each chromosome represents a complete potential solution.
    NOTE: Higher fitness scores are WORSE. The best fitness score is 0
    '''
    def __init__(self, _lstGenes):
        """
        Each chromosome represents a single potential solution
        """
        # each chromosome is a collection of individual 'genes' that make up
        # the solution
        self.genes = _lstGenes

    def printChromosome(self, _verbose=False):
        '''
        Print the contents of each chromosome.
        '''
        # print out the value of each gene in the chromosome
        for gene in self.genes:
            gene.printGene(_verbose)
        # print out the fitness score
        print "fitness = " + str(self.fitness())

    def __cmp__(self, _other):
        """
        Compare two chromosomes based on fitness
        :param other:
        :return:
        """
        return cmp(self.fitness(), _other.fitness())

    def __ne__(self, other):
        '''
        Test whether two chromosomes have different gene sequences (called by !=)
        '''
        return not self == other

    def __eq__(self, other):
        """
        Test whether two chromosomes have exactly the same gene sequence (called by ==)
        """
        # for each gene in each chromosome
        for g in range(len(self.genes)):
            # if any gene values don't match, then the chromosomes aren't equal
            if self.genes[g].value != other.genes[g].value:
                return False
        # everything matched, so the chromosomes are equal
        return True

    def randomValue(self, _lstDomain):
        """
        choose random values for each gene in the chromosome
        """
        # for each gene in the chromosome...
        for g in self.genes:
            # choose a random value for the gene
            g.value = g.randomValue()

    def fitness(self):
        """
        Calculate the 'fitness' of each chromosome, which represents how
        close the chromosome is to a valid solution
        """
        pass

    def crossOver(self, _other):
        """
        Given two chromosomes, 'mate' them and return two new chromosomes
        """
        # find the mid-point
        pivot = len(self.genes) / 2
        # swap the values around the mid-point
        newChrom1 = self.genes[0:pivot] + _other.genes[pivot:len(_other.genes)]
        newChrom2 = _other.genes[0:pivot] + self.genes[pivot:len(self.genes)]
        # return a tuple with the two new chromosomes
        return (newChrom1, newChrom2)

    def mutate(self):
        # choose a random gene
        geneIndex = random.randint(0, len(self.genes) - 1)
        # get a pointer to the gene
        gene = self.genes[geneIndex]
        # mutate the gene by choosing a random value
        gene.value = gene.randomValue()


class Population(object):
    def __init__(self, _populationSize, _chromosomeClass):
        """
        Create a class that holds the collection of chromosomes (the 'population')
        """
        # a generation is a collection of chromosomes ordered by fitness
        self.generation = []
        # store how many chromosomes are in each generation
        self.populationSize = _populationSize
        # store a template for generating chromosomes
        self.chromosomeClass = _chromosomeClass
        # choose a random starting population
        self.randomPopulation()

    def randomPopulation(self):
        # for each "slot" in the population queue
        for i in range(0, self.populationSize):
            # add a new, randomly-generated chromosome
            self.generation.append(self.chromosomeClass())
        # order by fitness
        self.generation.sort()

    def selection(self):
        """
        Decide which members of the population survive to the next generation
        """
        # pick top X of the population to survive
        for c in range(len(self.generation) / SELECTION_FRACTION, len(self.generation)):
            # remove the chromosome at the end (the lowest-ranked chromosome)
            chromosome = self.generation.pop()

    def crossOver(self):
        """
        Fill in the rest of the population by 'mating' pairs of chromosomes
        """
        # create an empty list for the new generation
        newGeneration = []
        # cross-over all chromosomes in turn - start with the beginning of the list
        for chrom1Index in range(0, len(self.generation)-1):
            # cross-over with all chromosomes that come after it
            for chrom2Index in range(chrom1Index, len(self.generation)):
                # get the chromosomes we are crossing over
                chrom1 = self.generation[chrom1Index]
                chrom2 = self.generation[chrom2Index]
                # perform the cross-over operation
                xOver = chrom1.crossOver(chrom2)
                # create two new chromosome objects
                newChrom1 = self.chromosomeClass()
                newChrom2 = self.chromosomeClass()
                # set their genes to the values created by crossover operation
                newChrom1.genes = xOver[0]
                newChrom2.genes = xOver[1]
                # save the new chromosomes we just created
                newGeneration.append(newChrom1)
                newGeneration.append(newChrom2)
        # for all the chromosomes we created through cross-over...
        for chromosome in newGeneration:
            # if we don't already have this chromosome
            if not chromosome in self.generation:
                # add it to our generation
                self.generation.append(chromosome)
        # as long as we haven't added more chromosomes than the population is supposed to have, create
        # random chromosomes
        while len(self.generation) < self.populationSize:
            # create a random chromosome
            newChromosome = self.chromosomeClass()
            # have we seen this chromosome before?
            if (not newChromosome in self.generation):
                # store it in our list of chromosomes
                self.generation.append(newChromosome)
        # make sure our list is ordered and not too big
        self.cleanUpGeneration()

    def mutate(self, _mutationProbability):
        # keep a list of all newly-created chromosomes
        newChromosomes = []
        # go through all the chromosomes in the current generation and call the mutate function on each
        for chromosome in self.generation:
            # roll the dice - are we going to mutate?
            if (random.random() < _mutationProbability):
                # make a copy of the chromosome
                newChromosome = copy.deepcopy(chromosome)
                # mutate the chromosome
                newChromosome.mutate()
                # keep the new chromosome
                newChromosomes.append(newChromosome)
        # add the newly-created chromosome to our generation
        for newChromosome in newChromosomes:
            # have we seen this chromosome before?
            if (not newChromosome in self.generation):
                # put the chromosome in the new generation
                self.generation.append(newChromosome)
        # make sure our list is ordered and not too big
        self.cleanUpGeneration()

    def cleanUpGeneration(self):
        # order by fitness
        self.generation.sort()
        # eliminate excess chromosomes
        while len(self.generation) > self.populationSize:
            self.generation.pop()

    def foundAWinner(self):
        foundWinner = False
        # go through all the chromosomes in the current generation and call the mutate function on each
        for chromosome in self.generation:
            # see if this matches
            if chromosome.fitness() == 0:
                foundWinner = True
        # report whether we found a winner
        return foundWinner

    def printSolutions(self):
        # go through all the chromosomes in the current generation and print each
        # chromosome with a fitness score of zero
        for chromosome in self.generation:
            # if it's a solution (i.e., fitness = 0)...
            if chromosome.fitness() == 0:
                # print the chromosome - True means print name and value for each gene
                chromosome.printChromosome(True)

    def printPopulation(self):
        # go through all the chromosomes in the current generation and print each
        for chromosome in self.generation:
            # print the chromosome
            chromosome.printChromosome()

def geneticAlgorithm(population, _mutationProbability=.2):
    loopCount = 0
    # print "starting"
    # population.printPopulation()
    # keep looping until we find a solution or we exceed our loop limit
    while (loopCount < LOOP_LIMIT):
        if (population.foundAWinner()):
            print "found a winner"
            population.printSolutions()
            return
        # selection
        population.selection()
        # print "selection"
        # population.printPopulation()
        # crossover
        population.crossOver()
        # print "crossover"
        # population.printPopulation()
        # mutation
        population.mutate(_mutationProbability)
        # print "mutation"
        # population.printPopulation()
        # increment loop count
        loopCount += 1
        if (loopCount % PRINT_FREQUENCY == 0):
            print "loop count = " + str(loopCount)
            population.printPopulation()

