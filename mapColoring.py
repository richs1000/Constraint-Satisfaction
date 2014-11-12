__author__ = 'rsimpson'

from constraintSatisfaction import *


class CSPGraphMapColoring(CSPGraph):
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



def MapColoring():
    # create a csp graph
    cspGraph = CSPGraphMapColoring()

    # add some variables
    cspGraph.addFeature('NSW', ['red', 'green', 'blue'])
    cspGraph.addFeature('V', ['red', 'green', 'blue'])
    cspGraph.addFeature('T', ['red', 'green', 'blue'])
    cspGraph.addFeature('WA', ['red', 'green', 'blue'])
    cspGraph.addFeature('NT', ['red', 'green', 'blue'])
    cspGraph.addFeature('SA', ['red', 'green', 'blue'])
    cspGraph.addFeature('Q', ['red', 'green', 'blue'])

    # add some constraints
    constraintList = [('WA', 'NT'), ('WA', 'SA'), ('Q', 'NT'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('NSW', 'V'), ('Q', 'NSW')]
    for constraintTuple in constraintList:
        ftrTail = constraintTuple[0]
        ftrHead = constraintTuple[1]
        strConstraint = '!='
        # create a new constraint object from tail to head
        newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrTail), strConstraint, cspGraph.getFeature(ftrHead))
        # put the new constraint in the graph's list of constraints
        cspGraph.constraints.append(newConstraint)
        # create a new constraint object from head to tail
        newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrHead), strConstraint, cspGraph.getFeature(ftrTail))
        # put the new constraint in the graph's list of constraints
        cspGraph.constraints.append(newConstraint)


    # call backtracking search
    #backtrackingSearch(cspGraph, 0)
    hillClimbingSearch(cspGraph)


MapColoring()