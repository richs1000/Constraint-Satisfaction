#
# Rich Simpson
# October 21, 2014
#
# This code is used in my CSCI 355 course. It implements
# constraint satisfaction problems

__author__ = 'rsimpson'


class CSPFeature:
    def __init__(self, strName, lstDomain):
        """
        Create a node object, which represents a feature/variable in the CSP graph.
        Set the name and domain of the feature.
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
    def __init__(self, lstFeatures, strConstraint):
        """
        Create a constraint object, which represents a constraint between
        multiple variables in the CSP graph
        """
        # store the list of feature objects involved in the constraint
        self.features = lstFeatures
        # store the constraint
        self.constraint = strConstraint

    def printConstraint(self):
        """
        Print the contents of  a constraint object
        """
        # start with an empty list of feature names
        featureNames = []
        # loop through all of the features associated with the constraint
        for feature in self.features:
            # add the feature name to the list of feature names
            featureNames.append(feature.name)
        # print out the names and the constraint
        print "Features = " + str(featureNames) + " Constraint = " + self.constraint

    def satisfied(self):
        """
        Returns true if constraint is satisfied and false if it is not. This
        gets replaced in the sub-classes that define each constraint.
        """
        return False


class CSPConstraintNotEqual(CSPConstraint):
    def __init__(self, lstFeatures, strConstraint):
        # call the parent constructor
        CSPConstraint.__init__(self, lstFeatures, strConstraint)

    def satisfied(self):
        """
        returns true if constraint is satisfied and false if it is not
        """
        # loop through all the features in the constraint
        for firstFeatureIndex in range(0,len(self.features)):
            # get the value of the next feature in the constraint
            firstFeatureValue = self.features[firstFeatureIndex].value
            # if this feature is unassigned then move on to the next feature, otherwise compare it to all
            # the features that come after it (we've already compared it to all the features that come
            # before it)
            if (firstFeatureValue != None):
                # loop through all the features that come after this one in the constraint
                for secondFeatureIndex in range(firstFeatureIndex+1, len(self.features)):
                    # get the value of the second feature in the constraint
                    secondFeatureValue = self.features[secondFeatureIndex].value
                    # if the feature is unassigned then move on to the next feature, otherwise make the
                    # comparison
                    if (secondFeatureValue != None):
                        # if both features are assigned and not equal then return false
                        if (firstFeatureValue == secondFeatureValue):
                            return False
        # otherwise, all features are assigned different values so return true
        return True


class CSPConstraintQueens(CSPConstraint):
    def __init__(self, lstFeatures, strConstraint, gridSize):
        # call the parent constructor
        CSPConstraint.__init__(self, lstFeatures, strConstraint)
        # define the grid size (assume it's a square) based on the number of features
        # (one feature for each queen means one feature for each row)
        self.gridSize = len(lstFeatures)
        # each list within this list will contain all the indexes for
        # a single diagonal on the board
        # I need to replace this with something that works for any size board - right
        # now this only works for 5x5 boards
        self.diagonals = [
            ['1', '5'],
            ['2', '6', '10'],
            ['3', '7', '11', '15'],
            ['4', '8', '12', '16', '20'],
            ['9', '13', '17', '21'],
            ['14', '18', '22'],
            ['19', '23'],
            ['3', '9'],
            ['2', '8', '14'],
            ['1', '7', '13', '19'],
            ['0', '6', '12', '18', '24'],
            ['5', '11', '17', '23'],
            ['10', '16', '22'],
            ['15', '21']
        ]
        # each list within this list will contain all the indexes for
        # a single column of the board
        self.columns = []
        # loop through all the columns in the board
        for col in range(0, gridSize):
            # start with an empty list
            columnList = []
            # loop through all the rows in the board
            for row in range(0, gridSize):
                # add the index of this row, col square
                columnList.append(str(col + row * gridSize))
            # add the list of indexes to the list of lists
            self.columns.append(columnList)

    def satisfied(self):
        """
        returns true if constraint is satisfied and false if it is not
        """
        # get position of first queen in constraint
        firstQueen = self.features[0].value
        # if the firstQueen value is unassigned then we're done
        if firstQueen == None:
            return True
        # get position of second queen in constraint
        secondQueen = self.features[1].value
        # if the secondQueen value is unassigned then we're done
        if secondQueen == None:
            return True
        # loop through the list of column lists
        for columnList in self.columns:
            # if both features are assigned and in the same column then return false
            if ((firstQueen in columnList) and (secondQueen in columnList)):
                return False
        # loop through the list of column lists
        for diagonalList in self.diagonals:
            # if both features are assigned and in the same column then return false
            if ((firstQueen in diagonalList) and (secondQueen in diagonalList)):
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
        Add a new variable to the list of variables
        """
        # check: does the variable already exist?
        # check: is the domain empty?
        # create a new variable CSPVariable object
        newFeature = CSPFeature(strName, lstDomain)
        # put the new variable in the graph's list of variables
        self.features.append(newFeature)

    def getFeature(self, featureName):
        # loop through all the existing features
        for feature in self.features:
            # when we have a match with the name
            if featureName == feature.name:
                # return the value in the solution
                return feature
        # feature doesn't exist
        return None

    def getConstraints(self, featureName):
        # start with an empty list of constraints
        lstConstraints = []
        # loop through all constraints
        for constraint in self.constraints:
            # loop through all the features effected by the constraint
            for feature in constraint.features:
                # if we have a match
                if featureName == feature.name:
                    # add the constraint to our list
                    lstConstraints.append(constraint)
        # return out list of constraints
        return lstConstraints

    def addConstraint(self, lstFeatureNames, strConstraint):
        # check: do all the variables exist?
        # check: does the constraint make sense?
        # create an empty list of feature objects
        lstFeatures = []
        # loop through the list of feature names and add the corresponding
        # feature objects to the list
        for featureName in lstFeatureNames:
            lstFeatures.append(self.getFeature(featureName))
        # create a new CSPConstraint object
        if (strConstraint == "!="):
            newConstraint = CSPConstraintNotEqual(lstFeatures, strConstraint)
        elif (strConstraint == "Queens"):
            newConstraint = CSPConstraintQueens(lstFeatures, strConstraint, 5)
        # put the new constraint in the graph's list of constraints
        self.constraints.append(newConstraint)

    def printGraph(self):
        print "-----"
        for feature in self.features:
            feature.printFeature()
        for constraint in self.constraints:
            constraint.printConstraint()
        print "-----"

    def printSolution(self):
        print "----- Solution -----"
        for feature in self.features:
            print "Name = " + feature.name + " Value = " + feature.value

    def satisfiesConstraints(self, feature):
        """
        This function tests a feature's value against all of the constraints. It
        returns true if the variable/value does not violate any of the constraints.
        """
        # get a list of relevant constraints
        lstConstraints = self.getConstraints(feature.name)
        # loop through all of the relevant constraints
        for constraint in lstConstraints:
            if (not constraint.satisfied()):
                return False
        # no violations, so return true
        return True

    def backtrackingSearch(self, featureIndex):
        """
        Basic backtracking search
        """
        # if the variableIndex exceeds the total number of variables then
        # we've found an assignment for each variable and we're done
        if (featureIndex >= len(self.features)):
            # print solution
            self.printSolution()
            # return True
            exit()
        # pick a feature f to assign next
        nextFeature = self.features[featureIndex]
        # start with the first value in the feature's domain
        domainIndex = 0
        # loop until we find a solution or we run out of values in
        # the domain of f
        while domainIndex < len(nextFeature.domain):
            # pick a value for the feature
            nextFeature.value = nextFeature.domain[domainIndex]
            # if the value satisfies all the constraints
            if self.satisfiesConstraints(nextFeature):
                # go to the next variable
                self.backtrackingSearch(featureIndex+1)
            # move on to the next value within the domain
            domainIndex += 1



# create a csp graph
cspGraph = CSPGraph()


# add some variables
# cspGraph.addFeature('WA', ['red', 'green', 'blue'])
# cspGraph.addFeature('NT', ['red', 'green', 'blue'])
# cspGraph.addFeature('SA', ['red', 'green', 'blue'])
# cspGraph.addFeature('Q', ['red', 'green', 'blue'])
# cspGraph.addFeature('NSW', ['red', 'green', 'blue'])
# cspGraph.addFeature('V', ['red', 'green', 'blue'])
# cspGraph.addFeature('T', ['red', 'green', 'blue'])
cspGraph.addFeature('Q1', ['0', '1', '2', '3', '4'])
cspGraph.addFeature('Q2', ['5', '6', '7', '8', '9'])
cspGraph.addFeature('Q3', ['10', '11', '12', '13', '14'])
cspGraph.addFeature('Q4', ['15', '16', '17', '18', '19'])
cspGraph.addFeature('Q5', ['20', '21', '22', '23', '24'])


# add some constraints
# cspGraph.addConstraint(['WA', 'NT'], '!=')
# cspGraph.addConstraint(['WA', 'SA'], '!=')
# cspGraph.addConstraint(['Q', 'NT'], '!=')
# cspGraph.addConstraint(['SA', 'NT'], '!=')
# cspGraph.addConstraint(['SA', 'Q'], '!=')
# cspGraph.addConstraint(['SA', 'NSW'], '!=')
# cspGraph.addConstraint(['SA', 'V'], '!=')
# cspGraph.addConstraint(['NSW', 'V'], '!=')
# cspGraph.addConstraint(['Q', 'NSW'], '!=')
cspGraph.addConstraint(['Q1', 'Q2'], 'Queens')
cspGraph.addConstraint(['Q1', 'Q3'], 'Queens')
cspGraph.addConstraint(['Q1', 'Q4'], 'Queens')
cspGraph.addConstraint(['Q1', 'Q5'], 'Queens')
cspGraph.addConstraint(['Q2', 'Q3'], 'Queens')
cspGraph.addConstraint(['Q2', 'Q4'], 'Queens')
cspGraph.addConstraint(['Q2', 'Q5'], 'Queens')
cspGraph.addConstraint(['Q3', 'Q4'], 'Queens')
cspGraph.addConstraint(['Q3', 'Q5'], 'Queens')
cspGraph.addConstraint(['Q4', 'Q5'], 'Queens')

#cspGraph.printGraph()

# call backtracking search
cspGraph.backtrackingSearch(0)