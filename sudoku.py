__author__ = 'rsimpson'

from constraintSatisfaction import *

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


class CSPGraphSudoku(CSPGraph):
    def __init__(self):
        # call parent constructor
        CSPGraph.__init__(self)


def createNotEqualConstraints(_cellList, _cspGraph):
    '''
    cellList contains a list of lists. Each sublist is a list of cells that should not be equal.
    This function creates the constraint objects to implement the not-equals constraints.
    '''
    # for each list of cells in a single column (or row, or square)...
    for cells in _cellList:
        # get a cell...
        for c1 in range(0, len(cells)-1):
            # create a not equal constraint for all the cells after it in the list
            for c2 in range(c1+1, len(cells)):
                # get the two cells we're creating a constraint for
                ftrTail = cells[c1]
                ftrHead = cells[c2]
                # create a new constraint object from tail to head
                newConstraint = CSPConstraintNotEqual(_cspGraph.getFeature(ftrTail), '!=', _cspGraph.getFeature(ftrHead))
                # put the new constraint in the graph's list of constraints
                _cspGraph.addConstraint(newConstraint)
                # create a new constraint object from head to tail
                newConstraint = CSPConstraintNotEqual(_cspGraph.getFeature(ftrHead), '!=', _cspGraph.getFeature(ftrTail))
                # put the new constraint in the graph's list of constraints
                _cspGraph.addConstraint(newConstraint)


class CSPFeatureGridCell(CSPFeature):
    def __init__(self, _strName, _lstDomain):
        # call parent constructor
        CSPFeature.__init__(self, _strName, _lstDomain)


def sudoku():
    # create a csp graph
    cspGraph = CSPGraphSudoku()

    # add some variables
    # 0  1  4  5
    # 2  3  6  7
    # 8  9 12 13
    #10 11 14 15
    cspGraph.addFeature(CSPFeatureGridCell('0', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('1', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('2', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('3', range(1, 5)))

    cspGraph.addFeature(CSPFeatureGridCell('4', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('5', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('6', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('7', range(1, 5)))

    cspGraph.addFeature(CSPFeatureGridCell('8', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('9', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('10', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('11', range(1, 5)))

    cspGraph.addFeature(CSPFeatureGridCell('12', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('13', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('14', range(1, 5)))
    cspGraph.addFeature(CSPFeatureGridCell('15', range(1, 5)))

    #
    # add not-equal constraints
    #
    # this is a list of all the cells in each column of the grid
    colList = [['0', '2', '8', '10'], ['1', '3', '9', '11'], ['4', '6', '12', '14'], ['5', '7', '13', '15']]
    createNotEqualConstraints(colList, cspGraph)
    # this is a list of all the cells in each row of the grid
    rowList = [['0', '1', '4', '5'], ['2', '3', '6', '7'], ['8', '9', '12', '13'], ['10', '11', '14', '15']]
    createNotEqualConstraints(rowList, cspGraph)
    # this is a list of all the cells in each 2x2 square within the grid
    sqrList = [['0', '1', '2', '3'], ['4', '5', '6', '7'], ['8', '9', '10', '11'], ['12', '13', '14', '15']]
    createNotEqualConstraints(sqrList, cspGraph)

    #hillClimbingSearch(cspGraph)
    backtrackingSearch(cspGraph)


sudoku()
