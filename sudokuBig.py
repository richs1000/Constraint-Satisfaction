__author__ = 'rsimpson'

from constraintSatisfaction import *
from math import sqrt


# This variable defines the size of the grids within the Sudoku puzzle - N x N x N (N grids, each with NxN cells)
# This value needs to have an integer square root, i.e., 4, 9, 16, 25...
gridSize = 4

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
                ftrTail = str(cells[c1])
                ftrHead = str(cells[c2])
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

    # add a feature for every cell in the puzzle
    # the puzzle consists of a GxG puzzle with G^2 grids of size NxN
    for row in range(0, gridSize):
        for col in range(0, gridSize):
            # cell name is a combination of grid, row and column
            cellName = str(row * gridSize + col)
            # create a feature corresponding to the cell
            cspGraph.addFeature(CSPFeatureGridCell(cellName, range(1, gridSize + 1)))

    #
    # add not-equal constraints
    #
    #
    # start with column constraints
    #
    # begin with an empty list
    colList = []
    # fill the list with an empty list for each column in the puzzle
    for c in range(0, gridSize):
        # add an empty list
        colList.append([])
    # for each row...
    for row in range(0, gridSize):
        # for each column...
        for col in range(0, gridSize):
            # cell name is a combination of grid, row and column
            cellName = row * gridSize + col
            # add the cell name to the correct sub-list
            colList[col].append(cellName)
    #
    # row constraints
    #
    # begin with an empty list
    rowList = []
    # fill the list with an empty list for each row in the puzzle
    for r in range(0, gridSize):
        # add a list with all the cells in a single row
        rowList.append(range(r * gridSize, r * gridSize + gridSize))
    #
    # sub-grid constraints
    #
    # start with an empty list
    sqrList = []
    # fill the list with an empty list for each sub-grid in the puzzle
    for s in range(0, gridSize):
        # add an empty list
        sqrList.append([])
    # the number of sqrs in each row and column is the square-root of the total grid size
    sqrSize = int(sqrt(gridSize))
    # for each row of squares...
    for sqrRow in range(0, sqrSize):
        # for each column of squares...
        for sqrCol in range(0, sqrSize):
            # for each row within the square
            for row in range(0, sqrSize):
                # for each column within the square
                for col in range(0, sqrSize):
                    # cell name is a combination of grid, row and column
                    cellName = sqrRow*gridSize*sqrSize + sqrCol*sqrSize + row*gridSize + col
                    # add the cell name to the correct sub-list
                    sqrList[sqrRow*sqrSize + sqrCol].append(cellName)
    # this is a list of all the cells in each column of the grid
    #colList = [['0', '2', '8', '10'], ['1', '3', '9', '11'], ['4', '6', '12', '14'], ['5', '7', '13', '15']]
    createNotEqualConstraints(colList, cspGraph)
    # this is a list of all the cells in each row of the grid
    #rowList = [['0', '1', '4', '5'], ['2', '3', '6', '7'], ['8', '9', '12', '13'], ['10', '11', '14', '15']]
    createNotEqualConstraints(rowList, cspGraph)
    # this is a list of all the cells in each 2x2 square within the grid
    #sqrList = [['0', '1', '2', '3'], ['4', '5', '6', '7'], ['8', '9', '10', '11'], ['12', '13', '14', '15']]
    createNotEqualConstraints(sqrList, cspGraph)

    hillClimbingSearch(cspGraph)
    #backtrackingSearch(cspGraph)


sudoku()
