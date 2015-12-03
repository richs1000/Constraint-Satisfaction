__author__ = 'rsimpson'

from constraintSatisfaction import *


class CSPGraphMapColoring(CSPGraph):
    def __init__(self):
        # call parent constructor
        CSPGraph.__init__(self)


class CSPFeatureState(CSPFeature):
    def __init__(self, _strName, _lstDomain):
        # call parent constructor
        CSPFeature.__init__(self, _strName, _lstDomain)


def MapColoring():
    # create a csp graph
    cspGraph = CSPGraphMapColoring()

    # add some variables
    cspGraph.addFeature(CSPFeatureState('NSW', ['red', 'green', 'blue']))
    cspGraph.addFeature(CSPFeatureState('V', ['red', 'green', 'blue']))
    cspGraph.addFeature(CSPFeatureState('T', ['red', 'green', 'blue']))
    cspGraph.addFeature(CSPFeatureState('WA', ['red', 'green', 'blue']))
    cspGraph.addFeature(CSPFeatureState('NT', ['red', 'green', 'blue']))
    cspGraph.addFeature(CSPFeatureState('SA', ['red', 'green', 'blue']))
    cspGraph.addFeature(CSPFeatureState('Q', ['red', 'green', 'blue']))

    # add some constraints
    constraintList = [('WA', 'NT'), ('WA', 'SA'), ('Q', 'NT'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('NSW', 'V'), ('Q', 'NSW')]
    for constraintTuple in constraintList:
        ftrTail = constraintTuple[0]
        ftrHead = constraintTuple[1]
        strConstraint = '!='
        # create a new constraint object from tail to head
        newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrTail), strConstraint, cspGraph.getFeature(ftrHead))
        # put the new constraint in the graph's list of constraints
        cspGraph.addConstraint(newConstraint)
        # create a new constraint object from head to tail
        newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrHead), strConstraint, cspGraph.getFeature(ftrTail))
        # put the new constraint in the graph's list of constraints
        cspGraph.addConstraint(newConstraint)


    # call backtracking search
    #backtrackingSearch(cspGraph)
    hillClimbingSearch(cspGraph)


MapColoring()