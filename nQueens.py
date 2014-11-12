__author__ = 'rsimpson'

from constraintSatisfaction import *

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


class CSPGraphQueens(CSPGraph):
    def __init__(self):
        # call parent constructor
        CSPGraph.__init__(self)

    def objectiveFunction(self):
        """
        Returns a measure of how 'good' the current solution is
        """
        # start at zero
        satisfiedConstraints = 0
        # loop through all of the constraints
        for constraint in self.constraints:
            # if the constraint is satisfied, then increase the count
            if (constraint.satisfied(constraint.tail.value, constraint.head.value)):
                satisfiedConstraints += 1
        # return the count of satisfied constraints
        return satisfiedConstraints


def NQueens():
    # initialize n-queens global variables
    createNQueensGlobals()

    # create a csp graph
    cspGraph = CSPGraphQueens()

    # add some variables
    for queen in range(0, GRIDSIZE):
        cspGraph.addFeature('Q'+str(queen), range(queen*GRIDSIZE, (queen+1)*GRIDSIZE))

    # add constraints
    for q1 in range(0, GRIDSIZE):
        for q2 in range(q1+1, GRIDSIZE):
#            cspGraph.addConstraint('Q'+str(q1), 'Queens', 'Q'+str(q2))
            ftrTail = 'Q' + str(q1)
            ftrHead = 'Q' + str(q2)
            strConstraint = 'Queens'
            # create a new constraint object from tail to head
            newConstraint = CSPConstraintQueens(cspGraph.getFeature(ftrTail), strConstraint, cspGraph.getFeature(ftrHead))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)
            # create a new constraint object from head to tail
            newConstraint = CSPConstraintQueens(cspGraph.getFeature(ftrHead), strConstraint, cspGraph.getFeature(ftrTail))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)


    # call backtracking search
    #backtrackingSearch(cspGraph, 0)
    hillClimbingSearch(cspGraph)

NQueens()
