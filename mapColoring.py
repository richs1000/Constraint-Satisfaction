__author__ = 'rsimpson'

from constraintSatisfaction import *


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
    backtrackingSearch(cspGraph, 0)
    #hillClimbingSearch(cspGraph)


MapColoring()