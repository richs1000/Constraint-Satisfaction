__author__ = 'rsimpson'


#
# Rich Simpson
# Nov 1, 2014
#
# This code is used in my CSCI 355 course. It implements constraint satisfaction
# problems. This version of the code only uses binary constraints.

__author__ = 'rsimpson'

#from nflSchedule import *

import copy
import random


# This flag is used to turn on forward checking
FORWARD_CHECKING = False

# This flag is used to turn on arc consistency
ARC_CONSISTENCY = True

# This flag is used to turn on variable ordering
VARIABLE_ORDERING = True

# This variable sets the limit for how many comparisons can be made before we give up
# on finding a better neighbor in hill-climbing search
COMPARISON_LIMIT = 1000

# This variable sets the limit for the total number of times through the hill-climbing
# loop before we give up
LOOP_LIMIT = 20000

# This variable keeps track of the probability of making a big jump
jumpProbability = 0.1

# This variable keeps track of the size of the jump
jumpSize = 5

# This variable determines how often we reduce the jump probability
jumpCounter = 1000

class CSPFeature:
    def __init__(self, strName, lstDomain):
        """
        Create a feature object, which represents a feature/variable in the CSP graph.
        Set the name and domain of the feature. The value starts out as unassigned.
        """
        # assign the name of the feature represented by the node
        self.name = str(strName)
        # assign the domain of the feature
        self.domain = lstDomain
        # the value starts out as undefined
        self.value = "none"

    def printFeature(self):
        print "Name = " + self.name + " Domain = " + str(self.domain) + " Value = " + self.value


class CSPConstraint:
    def __init__(self, ftrTail, strConstraint, ftrHead):
        """
        Create a binary constraint object, which represents a constraint between
        two variables in the CSP graph
        """
        # the tail feature of the constraint is the "left side" of the constraint
        # (i.e., tail < head for the "less than" constraint
        self.tail = ftrTail
        # the head feature of the constraint is the "right side" of the constraint
        # (i.e., tail < head for the "less than" constraint
        self.head = ftrHead
        # store the constraint
        self.constraint = strConstraint

    def printConstraint(self):
        """
        Print the contents of  a constraint object
        """
        # print out the names and the constraint
        print self.tail.name + " " + self.constraint + " " + self.head.name

    def satisfied(self, tailValue, headValue):
        """
        Returns true if constraint is satisfied and false if it is not. This
        gets replaced in the sub-classes that define each constraint.
        """
        return False


class CSPConstraintNotEqual(CSPConstraint):
    def __init__(self, ftrTail, strConstraint, ftrHead):
        # call the parent constructor
        CSPConstraint.__init__(self, ftrTail, strConstraint, ftrHead)

    def satisfied(self, tailValue, headValue):
        """
        returns false if head and tail features have the same value and true if they have
        different values or one of the features does not have a value
        """
        # if the head or the tail haven't been assigned, then the constraint is satisfied
        if headValue == "none" or tailValue == "none":
            return True
        # if both the head and the tail have been assigned and they have different values
        # then the constraint is satisfied
        if headValue != tailValue:
            return True
        # otherwise, they have the same value so the constraint is not satisfied
        return False



class CSPGraph:
    def __init__(self):
        """
        Create an empty CSP graph. A CSP graph consists of nodes (features)
        and edges (constraints).
        """
        # Create an empty list of features
        self.features = []
        # Create an empty list of edges
        self.constraints = []

    def addFeature(self, strName, lstDomain):
        """
        Add a new feature to the list of features
        """
        # create a new variable CSPVariable object
        newFeature = CSPFeature(strName, lstDomain)
        # put the new variable in the graph's list of variables
        self.features.append(newFeature)

    def getFeature(self, featureName):
        """
        Returns a pointer to the feature object with the name passed in as
        an argument
        """
        # loop through all the existing features
        for feature in self.features:
            # when we have a match with the name
            if featureName == feature.name:
                # return the value in the solution
                return feature
        # feature doesn't exist
        return None

    def getConstraints(self, featureName):
        """
        Returns a lists of constraints that have the feature name in either
        the head or the tail
        """
        # start with an empty list of constraints
        lstConstraints = []
        # loop through all constraints
        for constraint in self.constraints:
            # if the feature name appears in the tail of the constraint
            if featureName == constraint.tail.name:
                # add the constraint to our list
                lstConstraints.append(constraint)
            # if the feature name appears in the head of the constraint
            if featureName == constraint.head.name:
                # add the constraint to our list
                lstConstraints.append(constraint)
        # return our list of constraints
        return lstConstraints

    def getTailConstraints(self, featureName):
        """
        Returns a list of constraints that have the feature name in the
        tail. I need this for forward checking
        """
        # start with an empty list of constraints
        lstConstraints = []
        # loop through all constraints
        for constraint in self.constraints:
            # if the feature name appears in the tail of the constraint
            if featureName == constraint.tail.name:
                # add the constraint to our list
                lstConstraints.append(constraint)
        # return our list of constraints
        return lstConstraints

    def getHeadConstraints(self, featureName):
        """
        Returns a list of constraints that have the feature name in the
        head. I need this for arc consistency
        """
        # start with an empty list of constraints
        lstConstraints = []
        # loop through all constraints
        for constraint in self.constraints:
            # if the feature name appears in the tail of the constraint
            if featureName == constraint.head.name:
                # add the constraint to our list
                lstConstraints.append(constraint)
        # return our list of constraints
        return lstConstraints

    def printGraph(self):
        """
        Display the contents of the graph on the console
        """
        print "-----"
        for feature in self.features:
            feature.printFeature()
        for constraint in self.constraints:
            constraint.printConstraint()
        print "-----"

    def printSolution(self):
        """
        Display the values assigned to each feature in the CSP graph
        """
        print "----- Solution -----"
        for feature in self.features:
            print "Name = " + feature.name + " Value = " + str(feature.value)

    def satisfiesConstraints(self, feature):
        """
        This function tests a feature's value against all of the constraints. It
        returns true if the variable/value does not violate any of the constraints.
        """
        # get a list of relevant constraints
        lstConstraints = self.getConstraints(feature.name)
        # loop through all of the relevant constraints
        for constraint in lstConstraints:
            # if any of the constraints are not satisfied, then return False
            if (not constraint.satisfied(constraint.tail.value, constraint.head.value)):
                return False
        # no violations, so return true
        return True

    def forwardChecking(self, tailFeature):
        """
        This function goes through the list of all constraints and removes the
        value assigned to tailFeature from the domain of each feature connected
        to the tail feature
        """
        # get a list of constraints which have tailFeature in the tail
        lstConstraints = self.getTailConstraints(tailFeature.name)
        # loop through all of the relevant constraints
        for constraint in lstConstraints:
            # make a copy of the head domain to loop through
            headDomain = constraint.head.domain[:]
            # check each value in the domain of the constraint's head feature to see if it conflicts
            # with the value of the tail feature
            for headValue in headDomain:
                # if this value doesn't satisfy the constraint then remove the value from the domain
                if (not constraint.satisfied(tailFeature.value, headValue)):
                    # remove the value from the domain
                    constraint.head.domain.remove(headValue)

    def arcConsistency(self, constraint):
        """
        This function checks an individual arc for consistency, and then removes values
        from the domain of the tail feature if the arc is not consistent
        """
        # start out assuming the constraint is satisfied
        satisfied = True
        # if the tail is assigned then we don't need to do anything
        if (constraint.tail.value != "none"):
            # the arc is consistent
            return satisfied
        # if the head is assigned a value then we compare the tail domain to the assigned value
        if (constraint.head.value != "none"):
            # make a copy of the tail domain to loop through
            tailDomain = constraint.tail.domain[:]
            # loop through all values in the tail domain
            for tailValue in tailDomain:
                # if this value doesn't satisfy the constraint then remove the value from the domain
                if (not constraint.satisfied(tailValue, constraint.head.value)):
                    # record that the constraint wasn't satisfied
                    satisfied = False
                    # remove the value from the domain
                    constraint.tail.domain.remove(tailValue)
            # return whether or not the constraint was satisfied
            return satisfied
        # if the head is not assigned a value then we compare the tail domain to each value in the head domain
        # start assuming the tail domain has not been modified
        domainModified = False
        # make a copy of the tail domain to loop through
        tailDomain = constraint.tail.domain[:]
        # loop through all values in the tail domain
        for tailValue in tailDomain:
            # start out assuming the constraint is not satisfied
            satisfied = False
            # loop through all values in the head domain
            for headValue in constraint.head.domain:
                # does this value satisfy the constraint
                if (constraint.satisfied(tailValue, headValue)):
                    # record that the constraint wasn't satisfied
                    satisfied = True
            # if we didn't find a value in the head that works with the tail value
            if (not satisfied):
                # remove the tail value from the domain
                constraint.tail.domain.remove(tailValue)
                # mark that we removed something from the tail domain
                domainModified = True
        # return whether or not the constraint was satisfied
        return (not domainModified)

    def graphConsistency(self, feature):
        """
        This function creates a list of all the constraints in the graph, and enforces
        arc consistency for each one
        """
        # get a list of all constraints in which feature appears in the head
        headConstraints = self.getHeadConstraints(feature.name)
        # make a copy of the constraints list - we will treat this like a stack
        constraintList = headConstraints[:]
        # loop through all the constraints
        while len(constraintList) > 0:
            if (len(constraintList) % 10 == 0):
                print "\tconsistency checking constraints = " + str(len(constraintList))
            # grab a constraint off the stack
            constraint = constraintList.pop()
            # check the constraint for arc consistency
            consistent = self.arcConsistency(constraint)
            # if we removed all the values from the domain of the tail then we need to backtrack
            if (len(constraint.tail.domain) == 0):
                return False
            # if the arc wasn't consistent then we need to add back all the constraints
            # with a head equal to the tail of the changed constraint to the queue
            if (not consistent):
                # get a list of constraints where the tail feature we just changed appears as
                # the head
                reCheckConstraints = self.getHeadConstraints(constraint.tail.name)
                # go through the list, add back all constraints that are not already in the stack
                for c in reCheckConstraints:
                    # if the constraint is not already in the stack
                    if not c in constraintList:
                        # put it at the bottom of the stack
                        constraintList.insert(0, c)
        return True

    def getOpenConstraints(self, featureName):
        """
        Returns a lists of constraints that have the feature name in either
        the head or the tail and an unassigned feature in the other half of
        the constraint. This is used in mostConstrainingFeature()
        """
        # start with an empty list of constraints
        lstConstraints = []
        # loop through all constraints
        for constraint in self.constraints:
            # if the feature name appears in the tail of the constraint and the head constraint
            # is unassigned
            if (featureName == constraint.tail.name) and (constraint.head.value == 'none'):
                # add the constraint to our list
                lstConstraints.append(constraint)
            # if the feature name appears in the head of the constraint and the tail constraint
            # is unassigned
            if (featureName == constraint.head.name) and (constraint.tail.value == 'none'):
                # add the constraint to our list
                lstConstraints.append(constraint)
        # return our list of constraints
        return lstConstraints

    def mostConstrainingFeature(self):
        """
        Choose the feature with the most constraints on remaining unassigned features
        """
        # keep track of which feature we'll choose next
        nextFeature = None
        # a counter for the minimum number of constraints
        maxCount = -1
        # loop through all the features
        for feature in self.features:
            # if this feature has a value then go back to the top of the loop and get
            # the next feature
            if (feature.value != 'none'):
                continue
            # get a list of all the constraints involving this feature
            constraintList = self.getOpenConstraints(feature.name)
            # compare the number of constraints involving this feature to the current max
            # if this is the first unassigned feature we found or this feature has the most
            # constraints we've found...
            if (len(constraintList) > maxCount):
                # save a pointer to the current feature with most constraints
                nextFeature = feature
                # save the max number of constraints
                maxCount = len(constraintList)
        # return the least constraining feature
        return nextFeature

    def allConstraintsSatisfied(self):
        """
        This function tests all the features against all of the constraints. It
        returns true if the current set of feature assignments does not violate any
        of the constraints.
        """
        # loop through all of the constraints
        for constraint in self.constraints:
            # if any of the constraints are not satisfied, then return False
            if (not constraint.satisfied(constraint.tail.value, constraint.head.value)):
                return False
        # no violations, so return true
        return True

    def randomSolution(self):
        """
        This chooses a value for each feature randomly
        """
        # seed the random number generator
        random.seed()
        # loop through all the features
        for feature in self.features:
            # pick a random number based on the size of the feature's domain
            domainIndex = random.randint(0, len(feature.domain) - 1)
            # assign the value from the domain
            feature.value = feature.domain[domainIndex]

    def objectiveFunction(self):
        """
        Returns a measure of how 'good' the current solution is
        """
        print "You need to create your own objective function"

    def jump(self):
        """
        Increment the value of several features
        """
        global jumpSize
        print "jumping..."
        # create a range that includes all the available feature indices
        featureIndices = range(0, len(self.features))
        # remove indices until there are only jumpSize left
        while len(featureIndices) > jumpSize:
            # choose a random index
            index = random.randint(0, len(featureIndices)-1)
            # remove that item from the list of indices
            del featureIndices[index]
        for featureIndex in featureIndices:
            # get a pointer to that feature
            feature = self.features[featureIndex]
            # pick a random number based on the size of the feature's domain
            domainIncrement = random.randint(0, len(feature.domain) - 1)
            # get the index within the domain of the current feature value
            domainIndex = feature.domain.index(feature.value)
            # go to a different value in the domain
            newDomainIndex = (domainIndex + domainIncrement) % len(feature.domain)
            # assign the value from the domain
            feature.value = feature.domain[newDomainIndex]

    def pickANeighbor(self):
        """
        Choose a feature and increment its value
        """
        # pick a random feature
        featureIndex = random.randint(0, len(self.features) - 1)
        # get a pointer to that feature
        feature = self.features[featureIndex]
        # pick a random number based on the size of the feature's domain
        domainIncrement = random.randint(0, len(feature.domain) - 1)
        # get the index within the domain of the current feature value
        domainIndex = feature.domain.index(feature.value)
        # go to a different value in the domain
        newDomainIndex = (domainIndex + domainIncrement) % len(feature.domain)
        # assign the value from the domain
        feature.value = feature.domain[newDomainIndex]
        # return the feature and value that changed
        return (featureIndex, domainIndex)


def hillClimbingSearch(cspGraph):
    # access global variables
    global COMPARISON_LIMIT, LOOP_LIMIT, jumpProbability, jumpSize, jumpCounter
    # keep track of number of times through the loop
    loopCount = 0
    # pick a random solution
    cspGraph.randomSolution()
    # print solution
    print "starting solution"
    cspGraph.printSolution()
    # keep track of how many neighbors have been compared to the current maximum
    neighborComparisons = 0
    # keep looping until you hit a local maximum
    while (not cspGraph.allConstraintsSatisfied() and neighborComparisons < COMPARISON_LIMIT and loopCount < LOOP_LIMIT):
        # increment the loop count
        loopCount += 1
        # change the simulated annealing parameters every 'jumpCounter' times through the loop
        if (loopCount % jumpCounter == 0):
            # reduce the probability of a jump
            jumpProbability = jumpProbability / 1.5
            # reduce the size of a jump
            if jumpSize > 2:
                jumpSize = jumpSize - 1
        # check whether we should make a simulated annealing jump
        if random.random() < jumpProbability:
            cspGraph.jump()
        # or just do another round of regular hill climbing
        else:
            # get the current objective function value
            oldObjectiveValue = cspGraph.objectiveFunction()
            # get a neighboring solution
            oldValueTuple = cspGraph.pickANeighbor()
            # if we found a better solution, then start over with the new solution
            if cspGraph.objectiveFunction() >= oldObjectiveValue:
                print "loop count = " + str(loopCount) + " total constraints = " + str(len(cspGraph.constraints)) + " obj1 = " + str(oldObjectiveValue) + " obj2 = " + str(cspGraph.objectiveFunction())
                print "swapping..."
                # reset the number of neighbor comparisons
                neighborComparisons = 0
            # otherwise, restore the old values and try again
            else:
                # increment the number of neighbor comparisons
                neighborComparisons += 1
                # get the index of the feature that was changed
                oldFeature = oldValueTuple[0]
                # get the old value for that feature
                oldValue = oldValueTuple[1]
                # restore that value
                cspGraph.features[oldFeature].value = cspGraph.features[oldFeature].domain[oldValue]
    # print solution
    if cspGraph.allConstraintsSatisfied():
        print "found a solution"
    else:
        print "I stopped here:"
    cspGraph.printSolution()


def backtrackingSearch(cspGraph, featureIndex):
    """
    Backtracking search with forward checking and arc consistency
    """
    # access global variables
    global FORWARD_CHECKING
    global ARC_CONSISTENCY
    global VARIABLE_ORDERING
    # if the variableIndex exceeds the total number of variables then
    # we've found an assignment for each variable and we're done
    if (featureIndex >= len(cspGraph.features)):
        # print solution
        cspGraph.printSolution()
        # return True
        exit()
    # pick a feature f to assign next
    if (VARIABLE_ORDERING):
        nextFeature = cspGraph.mostConstrainingFeature()
    else:
        nextFeature = cspGraph.features[featureIndex]
    # start with the first value in the feature's domain
    domainIndex = 0
    # loop until we find a solution or we run out of values in
    # the domain of f
    while domainIndex < len(nextFeature.domain):
        print "feature index = " + str(featureIndex)
        if (domainIndex % 5 == 0 or featureIndex == 51):
            print "\tdomain index = " + str(domainIndex)
        # pick a value for the feature
        nextFeature.value = nextFeature.domain[domainIndex]
        # if the value satisfies all the constraints
        if cspGraph.satisfiesConstraints(nextFeature):
            # make a copy of the cspGraph
            cspGraphCopy = copy.deepcopy(cspGraph)
            # call backtracking
            if (FORWARD_CHECKING):
                # do forward checking
                cspGraphCopy.forwardChecking(nextFeature)
                # go to the next variable
                backtrackingSearch(cspGraphCopy, featureIndex+1)
            elif (ARC_CONSISTENCY):
                # enforce arc consistency for the whole graph
                if (cspGraphCopy.graphConsistency(nextFeature)):
                    # go to the next variable
                    backtrackingSearch(cspGraphCopy, featureIndex+1)
            else:
                # go to the next variable
                backtrackingSearch(cspGraphCopy, featureIndex+1)
        # move on to the next value within the domain
        domainIndex += 1
    # reset the feature value to unassigned and "unwind" backtracking by one level
    nextFeature.value = "none"



