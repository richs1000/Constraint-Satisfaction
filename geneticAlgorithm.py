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
        # a generation is a collection of chromosomes stored in a priority queue
        # which is ordered by fitness
        self.generation = PriorityQueue()
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
            self.generation.put(self.chromosomeClass())


    def selection(self):
        """
        Decide which members of the population survive to the next generation
        """
        # create an empty priority queue for the new generation
        newGeneration = PriorityQueue()
        # pick top X of the population to survive
        for c in range(0, self.generation.qsize() / SELECTION_FRACTION):
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
        # copy all the chromosomes from the current generation to a regular python list
        # start with an empty list
        lstChromosomes = []
        # loop through all the items in the queue
        while not self.generation.empty():
            # take a chromosome off the queue
            chromosome = self.generation.get()
            # append the chromosome to the list
            lstChromosomes.append(chromosome)
        # create an empty priority queue for the new generation
        newGeneration = PriorityQueue()
        # cross-over all chromosomes in turn - start with the beginning of the list
        for chrom1Index in range(0, len(lstChromosomes)-1):
            # cross-over with all chromosomes that come after it
            for chrom2Index in range(chrom1Index, len(lstChromosomes)):
                # get the chromosomes we are crossing over
                chrom1 = lstChromosomes[chrom1Index]
                chrom2 = lstChromosomes[chrom2Index]
                # perform the cross-over operation
                xOver = chrom1.crossOver(chrom2)
                # create two new chromosome objects
                newChrom1 = self.chromosomeClass()
                newChrom2 = self.chromosomeClass()
                # set their genes to the values created by crossover operation
                newChrom1.genes = xOver[0]
                newChrom2.genes = xOver[1]
                # save the new chromosomes we just created
                newGeneration.put(newChrom1)
                newGeneration.put(newChrom2)
        # save all the original chromosomes
        for chromosome in lstChromosomes:
            newGeneration.put(chromosome)
        # keep track of all the chromosomes we create
        lstChromosomes = []
        # keep track of how many we are keeping
        chromosomesKept = 0
        # as long as we haven't added more chromosomes than the population is supposed to have
        # and we have more chromosomes to add...
        while chromosomesKept < self.populationSize and not newGeneration.empty():
            # take a chromosome off the new generation queue
            newChromosome = newGeneration.get()
            # have we seen this chromosome before?
            if (not newChromosome in lstChromosomes):
                # store it in our list of chromosomes
                lstChromosomes.append(newChromosome)
                # store it in the queue in the chromosome
                self.generation.put(newChromosome)
                # increase our count of chromosomes kept
                chromosomesKept += 1
        # as long as we haven't added more chromosomes than the population is supposed to have, create
        # random chromosomes
        while chromosomesKept < self.populationSize:
            # create a random chromosome
            newChromosome = self.chromosomeClass()
            # have we seen this chromosome before?
            if (not newChromosome in lstChromosomes):
                # store it in our list of chromosomes
                lstChromosomes.append(newChromosome)
                # store it in the queue in the chromosome
                self.generation.put(newChromosome)
                # increase our count of chromosomes kept
                chromosomesKept += 1

    def mutate(self, _mutationProbability):
        # create an empty priority queue for the new generation
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # roll the dice - are we going to mutate?
            if (random.random() > _mutationProbability):
                # make a copy of the chromosome
                newChromosome = copy.deepcopy(chromosome)
                # mutate the chromosome
                newChromosome.mutate()
                # put the chromosome in the new generation
                newGeneration.put(newChromosome)
        # keep the new generation
        self.generation = newGeneration

    def foundAWinner(self):
        foundWinner = False
        # create an empty priority queue
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and call the mutate function on each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # see if this matches
            if chromosome.fitness() == 0:
                foundWinner = True
            # put the chromosome in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration
        # report whether we found a winner
        return foundWinner

    def printSolutions(self):
        # create an empty priority queue
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and print each
        # chromosome with a fitness score of zero
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # if it's a solution (i.e., fitness = 0)...
            if chromosome.fitness() == 0:
                # print the chromosome - True means print name and value for each gene
                chromosome.printChromosome(True)
            # put the chromosome in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration

    def printPopulation(self):
        # create an empty priority queue
        newGeneration = PriorityQueue()
        # go through all the chromosomes in the current generation and print each
        while not self.generation.empty():
            # get another chromosome
            chromosome = self.generation.get()
            # print the chromosome
            chromosome.printChromosome()
            # put the chromosome in the new generation
            newGeneration.put(chromosome)
        # keep the new generation
        self.generation = newGeneration

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

