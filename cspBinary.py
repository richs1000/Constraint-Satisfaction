#
# Rich Simpson
# Nov 1, 2014
#
# This code is used in my CSCI 355 course. It implements constraint satisfaction
# problems. This version of the code only uses binary constraints.

__author__ = 'rsimpson'

import copy

# This value is used to determine the size of the board when doing an n-queens problem
GRIDSIZE = 16

# This is a list of lists - where each sub-list contains the indices that are in the
# same column.
NQUEENS_COLUMNS = []

# This is a list of lists - where each sub-list contains the indices that are in the
# same diagonal.
NQUEENS_DIAGONALS = []

# This flag is used to turn on forward checking
FORWARD_CHECKING = False

# This flag is used to turn on arc consistency
ARC_CONSISTENCY = True

# This flag is used to turn on variable ordering
VARIABLE_ORDERING = True

class CSPFeature:
    def __init__(self, strName, lstDomain):
        """
        Create a feature object, which represents a feature/variable in the CSP graph.
        Set the name and domain of the feature. The value starts out as unassigned.
        """
        # assign the name of the feature represented by the node
        self.name = strName
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


class CSPConstraintQueens(CSPConstraint):
    def __init__(self, ftrTail, strConstraint, ftrHead):
        """
        This function sets up the values for an N-Queens constraint. Right now, each constraint object
        stores its own column list and diagonal list, which is inefficient. I should really change this
        so I only store it once.
        """
        # access the global variables
        global GRIDSIZE
        global NQUEENS_DIAGONALS
        global NQUEENS_COLUMNS
        # call the parent constructor
        CSPConstraint.__init__(self, ftrTail, strConstraint, ftrHead)
        # define the grid size (assume it's a square) based on the number of features
        # (one feature for each queen means one feature for each row)
        self.gridSize = GRIDSIZE
        # store a pointer to the list of column lists
        self.columns = NQUEENS_COLUMNS
        # store a pointer to the list of diagonals
        self.diagonals = NQUEENS_DIAGONALS

    def satisfied(self, tailValue, headValue):
        """
        returns true if constraint is satisfied and false if it is not
        """
        # if the head value or tail value is unassigned then we're done
        if tailValue == "none" or headValue == "none":
            return True
        # loop through the list of column lists
        for columnList in self.columns:
            # if both features are assigned and in the same column then return false
            if ((int(tailValue) in columnList) and (int(headValue) in columnList)):
                return False
        # loop through the list of diagonal lists
        for diagonalList in self.diagonals:
            # if both features are assigned and in the same diagonal then return false
            if ((int(tailValue) in diagonalList) and (int(headValue) in diagonalList)):
                return False
        # otherwise, all constraints are satisfied so return true
        return True


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

    def addConstraint(self, ftrTail, strConstraint, ftrHead):
        """
        Creates a constraint object and adds it to the CSP graph. Depending on the type
        of constraint, the function will either create two matching constraint objects
        (one in each direction) or two complementary constraint objects (for example,
        a 'less-than' constraint in one direction and a 'greater-than' constraint in the
        other direction.
        """
        # create a new 'not-equal' CSPConstraint object
        if (strConstraint == "!=" or strConstraint == 'NotEqual'):
            # create a new constraint object from tail to head
            newConstraint = CSPConstraintNotEqual(self.getFeature(ftrTail), strConstraint, self.getFeature(ftrHead))
            # put the new constraint in the graph's list of constraints
            self.constraints.append(newConstraint)
            # create a new constraint object from head to tail
            newConstraint = CSPConstraintNotEqual(self.getFeature(ftrHead), strConstraint, self.getFeature(ftrTail))
            # put the new constraint in the graph's list of constraints
            self.constraints.append(newConstraint)
        # create a new 'NQueens' CSPConstraint object
        elif (strConstraint == "Queens"):
            # create a new constraint object from tail to head
            newConstraint = CSPConstraintQueens(self.getFeature(ftrTail), strConstraint, self.getFeature(ftrHead))
            # put the new constraint in the graph's list of constraints
            self.constraints.append(newConstraint)
            # create a new constraint object from head to tail
            newConstraint = CSPConstraintQueens(self.getFeature(ftrHead), strConstraint, self.getFeature(ftrTail))
            # put the new constraint in the graph's list of constraints
            self.constraints.append(newConstraint)

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

    def graphConsistency(self):
        """
        This function creates a list of all the constraints in the graph, and enforces
        arc consistency for each one
        """
        # make a copy of the constraints list - we will treat this like a stack
        constraintList = self.constraints[:]
        # loop through all the constraints
        while len(constraintList) > 0:
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
                if (cspGraphCopy.graphConsistency()):
                    # go to the next variable
                    backtrackingSearch(cspGraphCopy, featureIndex+1)
            else:
                # go to the next variable
                backtrackingSearch(cspGraphCopy, featureIndex+1)
        # move on to the next value within the domain
        domainIndex += 1
    # reset the feature value to unassigned and "unwind" backtracking by one level
    nextFeature.value = "none"



def NQueens():
    # initialize n-queens global variables
    createNQueensGlobals()

    # create a csp graph
    cspGraph = CSPGraph()

    # add some variables
    for queen in range(0, GRIDSIZE):
        cspGraph.addFeature('Q'+str(queen), range(queen*GRIDSIZE, (queen+1)*GRIDSIZE))

    # add constraints
    for q1 in range(0, GRIDSIZE):
        for q2 in range(q1+1, GRIDSIZE):
            cspGraph.addConstraint('Q'+str(q1), 'Queens', 'Q'+str(q2))

    # call backtracking search
    backtrackingSearch(cspGraph, 0)


def MapColoring():
    # create a csp graph
    cspGraph = CSPGraph()

    # add some variables
    cspGraph.addFeature('NSW', ['red', 'green', 'blue'])
    cspGraph.addFeature('V', ['red', 'green', 'blue'])
    cspGraph.addFeature('T', ['red', 'green', 'blue'])
    cspGraph.addFeature('WA', ['red', 'green', 'blue'])
    cspGraph.addFeature('NT', ['red', 'green', 'blue'])
    cspGraph.addFeature('SA', ['red', 'green', 'blue'])
    cspGraph.addFeature('Q', ['red', 'green', 'blue'])

    # add some constraints
    cspGraph.addConstraint('WA', '!=', 'NT')
    cspGraph.addConstraint('WA', '!=', 'SA')
    cspGraph.addConstraint('Q', '!=', 'NT')
    cspGraph.addConstraint('SA', '!=', 'NT')
    cspGraph.addConstraint('SA', '!=', 'Q')
    cspGraph.addConstraint('SA', '!=', 'NSW')
    cspGraph.addConstraint('SA', '!=', 'V')
    cspGraph.addConstraint('NSW', '!=', 'V')
    cspGraph.addConstraint('Q', '!=', 'NSW')

    # call backtracking search
    backtrackingSearch(cspGraph, 0)



NQueens()
#MapColoring()