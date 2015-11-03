__author__ = 'rsimpson'

from constraintSatisfaction import *

# This flag is used to turn on forward checking
FORWARD_CHECKING = False

# This flag is used to turn on arc consistency
ARC_CONSISTENCY = False

# This flag is used to turn on variable ordering
VARIABLE_ORDERING = False

class CSPGraphCampusLayout(CSPGraph):
    def __init__(self):
        # call parent constructor
        CSPGraph.__init__(self)

class CSPConstraintAdjacent(CSPConstraint):
    def __init__(self, ftrTail, strConstraint, ftrHead):
        """
        This class implements the constraint that two buildings be adjacent to each other on campus
        """
        # call the parent constructor
        CSPConstraint.__init__(self, ftrTail, strConstraint, ftrHead)

    def satisfied(self, tailValue, headValue):
        """
        returns true if constraint is satisfied and false if it is not
        """
        # if the head value or tail value is unassigned then we're done
        if tailValue == "none" or headValue == "none":
            return True
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

class CSPConstraintNotAdjacent(CSPConstraint):
    def __init__(self, ftrTail, strConstraint, ftrHead):
        """
        This class implements the constraint that two buildings be adjacent to each other on campus
        """
        # call the parent constructor
        CSPConstraint.__init__(self, ftrTail, strConstraint, ftrHead)

    def satisfied(self, tailValue, headValue):
        """
        returns true if constraint is satisfied and false if it is not
        """
        # if the head value or tail value is unassigned then we're done
        if tailValue == "none" or headValue == "none":
            return True
        if (tailValue == 1 and (headValue == 2 or headValue == 4)):
            return False
        elif ((tailValue == 2) and (headValue == 1 or headValue == 3 or headValue == 5)):
            return False
        elif ((tailValue == 3) and (headValue == 2 or headValue == 6)):
            return False
        elif ((tailValue == 4) and (headValue == 1 or headValue == 5)):
            return False
        elif ((tailValue == 5) and (headValue == 2 or headValue == 4 or headValue == 6)):
            return False
        elif ((tailValue == 6) and (headValue == 3 or headValue == 5)):
            return False
        # otherwise, constraint is not satisfied so return false
        return True

def CampusLayout():
    # create a csp graph
    cspGraph = CSPGraphCampusLayout()

    # add some variables
    cspGraph.addFeature('A', [1, 3, 5, 6])
    cspGraph.addFeature('B', [3, 6])
    cspGraph.addFeature('C', [1, 2, 3, 4, 5, 6])
    cspGraph.addFeature('D', [2, 3, 4, 6])

    #
    # add not-equal constraints
    #
    # start with a list of all unique combinations of features
    constraintList = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
    # loop through the list of feature pairs
    for constraintTuple in constraintList:
        # in some algorithms, constraints are uni-directional
        ftrTail = constraintTuple[0]
        ftrHead = constraintTuple[1]
        strConstraint = '!='
        # create a new constraint object from tail to head
        newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrTail), '!=', cspGraph.getFeature(ftrHead))
        # put the new constraint in the graph's list of constraints
        cspGraph.constraints.append(newConstraint)
        # create a new constraint object from head to tail
        newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrHead), '!=', cspGraph.getFeature(ftrTail))
        # put the new constraint in the graph's list of constraints
        cspGraph.constraints.append(newConstraint)

    #
    # Administration building (A) must be adjacent to the bus stop (B)
    #
    # create a new constraint object
    newConstraint = CSPConstraintAdjacent(cspGraph.getFeature('A'), 'adjacent', cspGraph.getFeature('B'))
    # put the new constraint in the graph's list of constraints
    cspGraph.constraints.append(newConstraint)

    #
    # Classroom (C) must be adjacent to the bus stop (B)
    #
    # create a new constraint object
    newConstraint = CSPConstraintAdjacent(cspGraph.getFeature('C'), 'adjacent', cspGraph.getFeature('B'))
    # put the new constraint in the graph's list of constraints
    cspGraph.constraints.append(newConstraint)

    #
    # Classroom (C) must be adjacent to the dormitory (D)
    #
    # create a new constraint object
    newConstraint = CSPConstraintAdjacent(cspGraph.getFeature('C'), 'adjacent', cspGraph.getFeature('D'))
    # put the new constraint in the graph's list of constraints
    cspGraph.constraints.append(newConstraint)

    #
    # Administration building (A) must NOT be adjacent to the dormitory (D)
    #
    # create a new constraint object
    newConstraint = CSPConstraintNotAdjacent(cspGraph.getFeature('A'), 'adjacent', cspGraph.getFeature('D'))
    # put the new constraint in the graph's list of constraints
    cspGraph.constraints.append(newConstraint)

    # call backtracking search
    backtrackingSearch(cspGraph, 0)
    #hillClimbingSearch(cspGraph)


CampusLayout()
