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
    backtrackingSearch(cspGraph)
    #hillClimbingSearch(cspGraph)


MapColoring()