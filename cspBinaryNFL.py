#
# Rich Simpson
# Nov 1, 2014
#
# This code is used in my CSCI 355 course. It implements constraint satisfaction
# problems. This version of the code only uses binary constraints.

__author__ = 'rsimpson'

import copy

NUMBER_OF_WEEKS = 4
GAMES_PER_WEEK = 16

nflGames = {
    '0':{'Away':'Bills', 'Home':'Bears','Conference':'AFC','TimeZone':'Central'},
    '1':{'Away':'Buccaneers', 'Home':'Bears','Conference':'NFC','TimeZone':'Central'},
    '2':{'Away':'Cowboys', 'Home':'Bears','Conference':'NFC','TimeZone':'Central'},
    '3':{'Away':'Dolphins', 'Home':'Bears','Conference':'AFC','TimeZone':'Central'},
    '4':{'Away':'Lions', 'Home':'Bears','Conference':'NFC','TimeZone':'Central'},
    '5':{'Away':'Packers', 'Home':'Bears','Conference':'NFC','TimeZone':'Central'},
    '6':{'Away':'Saints', 'Home':'Bears','Conference':'NFC','TimeZone':'Central'},
    '7':{'Away':'Vikings', 'Home':'Bears','Conference':'NFC','TimeZone':'Central'},
    '8':{'Away':'Broncos', 'Home':'Chiefs','Conference':'AFC','TimeZone':'Central'},
    '9':{'Away':'Chargers', 'Home':'Chiefs','Conference':'AFC','TimeZone':'Central'},
    '10':{'Away':'Jets', 'Home':'Chiefs','Conference':'AFC','TimeZone':'Central'},
    '11':{'Away':'Patriots', 'Home':'Chiefs','Conference':'AFC','TimeZone':'Central'},
    '12':{'Away':'Raiders', 'Home':'Chiefs','Conference':'AFC','TimeZone':'Central'},
    '13':{'Away':'Rams', 'Home':'Chiefs','Conference':'NFC','TimeZone':'Central'},
    '14':{'Away':'Seahawks', 'Home':'Chiefs','Conference':'NFC','TimeZone':'Central'},
    '15':{'Away':'Titans', 'Home':'Chiefs','Conference':'AFC','TimeZone':'Central'},
    '16':{'Away':'Bengals', 'Home':'Colts','Conference':'AFC','TimeZone':'Central'},
    '17':{'Away':'Eagles', 'Home':'Colts','Conference':'NFC','TimeZone':'Central'},
    '18':{'Away':'Jaguars', 'Home':'Colts','Conference':'AFC','TimeZone':'Central'},
    '19':{'Away':'Patriots', 'Home':'Colts','Conference':'AFC','TimeZone':'Central'},
    '20':{'Away':'Ravens', 'Home':'Colts','Conference':'AFC','TimeZone':'Central'},
    '21':{'Away':'Redskins', 'Home':'Colts','Conference':'NFC','TimeZone':'Central'},
    '22':{'Away':'Texans', 'Home':'Colts','Conference':'AFC','TimeZone':'Central'},
    '23':{'Away':'Titans', 'Home':'Colts','Conference':'AFC','TimeZone':'Central'},
    '24':{'Away':'49ers', 'Home':'Cowboys','Conference':'NFC','TimeZone':'Central'},
    '25':{'Away':'Cardinals', 'Home':'Cowboys','Conference':'NFC','TimeZone':'Central'},
    '26':{'Away':'Colts', 'Home':'Cowboys','Conference':'AFC','TimeZone':'Central'},
    '27':{'Away':'Eagles', 'Home':'Cowboys','Conference':'NFC','TimeZone':'Central'},
    '28':{'Away':'Giants', 'Home':'Cowboys','Conference':'NFC','TimeZone':'Central'},
    '29':{'Away':'Redskins', 'Home':'Cowboys','Conference':'NFC','TimeZone':'Central'},
    '30':{'Away':'Saints', 'Home':'Cowboys','Conference':'NFC','TimeZone':'Central'},
    '31':{'Away':'Texans', 'Home':'Cowboys','Conference':'AFC','TimeZone':'Central'},
    '32':{'Away':'Bears', 'Home':'Packers','Conference':'NFC','TimeZone':'Central'},
    '33':{'Away':'Eagles', 'Home':'Packers','Conference':'NFC','TimeZone':'Central'},
    '34':{'Away':'Falcons', 'Home':'Packers','Conference':'NFC','TimeZone':'Central'},
    '35':{'Away':'Jets', 'Home':'Packers','Conference':'AFC','TimeZone':'Central'},
    '36':{'Away':'Lions', 'Home':'Packers','Conference':'NFC','TimeZone':'Central'},
    '37':{'Away':'Panthers', 'Home':'Packers','Conference':'NFC','TimeZone':'Central'},
    '38':{'Away':'Patriots', 'Home':'Packers','Conference':'AFC','TimeZone':'Central'},
    '39':{'Away':'Vikings', 'Home':'Packers','Conference':'NFC','TimeZone':'Central'},
    '40':{'Away':'49ers', 'Home':'Rams','Conference':'NFC','TimeZone':'Central'},
    '41':{'Away':'Broncos', 'Home':'Rams','Conference':'AFC','TimeZone':'Central'},
    '42':{'Away':'Cardinals', 'Home':'Rams','Conference':'NFC','TimeZone':'Central'},
    '43':{'Away':'Cowboys', 'Home':'Rams','Conference':'NFC','TimeZone':'Central'},
    '44':{'Away':'Giants', 'Home':'Rams','Conference':'NFC','TimeZone':'Central'},
    '45':{'Away':'Raiders', 'Home':'Rams','Conference':'AFC','TimeZone':'Central'},
    '46':{'Away':'Seahawks', 'Home':'Rams','Conference':'NFC','TimeZone':'Central'},
    '47':{'Away':'Vikings', 'Home':'Rams','Conference':'NFC','TimeZone':'Central'},
    '48':{'Away':'49ers', 'Home':'Saints','Conference':'NFC','TimeZone':'Central'},
    '49':{'Away':'Bengals', 'Home':'Saints','Conference':'AFC','TimeZone':'Central'},
    '50':{'Away':'Buccaneers', 'Home':'Saints','Conference':'NFC','TimeZone':'Central'},
    '51':{'Away':'Falcons', 'Home':'Saints','Conference':'NFC','TimeZone':'Central'},
    '52':{'Away':'Packers', 'Home':'Saints','Conference':'NFC','TimeZone':'Central'},
    '53':{'Away':'Panthers', 'Home':'Saints','Conference':'NFC','TimeZone':'Central'},
    '54':{'Away':'Ravens', 'Home':'Saints','Conference':'AFC','TimeZone':'Central'},
    '55':{'Away':'Vikings', 'Home':'Saints','Conference':'NFC','TimeZone':'Central'},
    '56':{'Away':'Bengals', 'Home':'Texans','Conference':'AFC','TimeZone':'Central'},
    '57':{'Away':'Bills', 'Home':'Texans','Conference':'AFC','TimeZone':'Central'},
    '58':{'Away':'Colts', 'Home':'Texans','Conference':'AFC','TimeZone':'Central'},
    '59':{'Away':'Eagles', 'Home':'Texans','Conference':'NFC','TimeZone':'Central'},
    '60':{'Away':'Jaguars', 'Home':'Texans','Conference':'AFC','TimeZone':'Central'},
    '61':{'Away':'Ravens', 'Home':'Texans','Conference':'AFC','TimeZone':'Central'},
    '62':{'Away':'Redskins', 'Home':'Texans','Conference':'NFC','TimeZone':'Central'},
    '63':{'Away':'Titans', 'Home':'Texans','Conference':'AFC','TimeZone':'Central'},
    '64':{'Away':'Browns', 'Home':'Titans','Conference':'AFC','TimeZone':'Central'},
    '65':{'Away':'Colts', 'Home':'Titans','Conference':'AFC','TimeZone':'Central'},
    '66':{'Away':'Cowboys', 'Home':'Titans','Conference':'NFC','TimeZone':'Central'},
    '67':{'Away':'Giants', 'Home':'Titans','Conference':'NFC','TimeZone':'Central'},
    '68':{'Away':'Jaguars', 'Home':'Titans','Conference':'AFC','TimeZone':'Central'},
    '69':{'Away':'Jets', 'Home':'Titans','Conference':'AFC','TimeZone':'Central'},
    '70':{'Away':'Steelers', 'Home':'Titans','Conference':'AFC','TimeZone':'Central'},
    '71':{'Away':'Texans', 'Home':'Titans','Conference':'AFC','TimeZone':'Central'},
    '72':{'Away':'Bears', 'Home':'Vikings','Conference':'NFC','TimeZone':'Central'},
    '73':{'Away':'Falcons', 'Home':'Vikings','Conference':'NFC','TimeZone':'Central'},
    '74':{'Away':'Jets', 'Home':'Vikings','Conference':'AFC','TimeZone':'Central'},
    '75':{'Away':'Lions', 'Home':'Vikings','Conference':'NFC','TimeZone':'Central'},
    '76':{'Away':'Packers', 'Home':'Vikings','Conference':'NFC','TimeZone':'Central'},
    '77':{'Away':'Panthers', 'Home':'Vikings','Conference':'NFC','TimeZone':'Central'},
    '78':{'Away':'Patriots', 'Home':'Vikings','Conference':'AFC','TimeZone':'Central'},
    '79':{'Away':'Redskins', 'Home':'Vikings','Conference':'NFC','TimeZone':'Central'},
    '80':{'Away':'Broncos', 'Home':'Bengals','Conference':'AFC','TimeZone':'Eastern'},
    '81':{'Away':'Browns', 'Home':'Bengals','Conference':'AFC','TimeZone':'Eastern'},
    '82':{'Away':'Falcons', 'Home':'Bengals','Conference':'NFC','TimeZone':'Eastern'},
    '83':{'Away':'Jaguars', 'Home':'Bengals','Conference':'AFC','TimeZone':'Eastern'},
    '84':{'Away':'Panthers', 'Home':'Bengals','Conference':'NFC','TimeZone':'Eastern'},
    '85':{'Away':'Ravens', 'Home':'Bengals','Conference':'AFC','TimeZone':'Eastern'},
    '86':{'Away':'Steelers', 'Home':'Bengals','Conference':'AFC','TimeZone':'Eastern'},
    '87':{'Away':'Titans', 'Home':'Bengals','Conference':'AFC','TimeZone':'Eastern'},
    '88':{'Away':'Browns', 'Home':'Bills','Conference':'AFC','TimeZone':'Eastern'},
    '89':{'Away':'Chargers', 'Home':'Bills','Conference':'AFC','TimeZone':'Eastern'},
    '90':{'Away':'Chiefs', 'Home':'Bills','Conference':'AFC','TimeZone':'Eastern'},
    '91':{'Away':'Dolphins', 'Home':'Bills','Conference':'AFC','TimeZone':'Eastern'},
    '92':{'Away':'Jets', 'Home':'Bills','Conference':'AFC','TimeZone':'Eastern'},
    '93':{'Away':'Packers', 'Home':'Bills','Conference':'NFC','TimeZone':'Eastern'},
    '94':{'Away':'Patriots', 'Home':'Bills','Conference':'AFC','TimeZone':'Eastern'},
    '95':{'Away':'Vikings', 'Home':'Bills','Conference':'NFC','TimeZone':'Eastern'},
    '96':{'Away':'Bengals', 'Home':'Browns','Conference':'AFC','TimeZone':'Eastern'},
    '97':{'Away':'Buccaneers', 'Home':'Browns','Conference':'NFC','TimeZone':'Eastern'},
    '98':{'Away':'Colts', 'Home':'Browns','Conference':'AFC','TimeZone':'Eastern'},
    '99':{'Away':'Raiders', 'Home':'Browns','Conference':'AFC','TimeZone':'Eastern'},
    '100':{'Away':'Ravens', 'Home':'Browns','Conference':'AFC','TimeZone':'Eastern'},
    '101':{'Away':'Saints', 'Home':'Browns','Conference':'NFC','TimeZone':'Eastern'},
    '102':{'Away':'Steelers', 'Home':'Browns','Conference':'AFC','TimeZone':'Eastern'},
    '103':{'Away':'Texans', 'Home':'Browns','Conference':'AFC','TimeZone':'Eastern'},
    '104':{'Away':'Bengals', 'Home':'Buccaneers','Conference':'AFC','TimeZone':'Eastern'},
    '105':{'Away':'Falcons', 'Home':'Buccaneers','Conference':'NFC','TimeZone':'Eastern'},
    '106':{'Away':'Packers', 'Home':'Buccaneers','Conference':'NFC','TimeZone':'Eastern'},
    '107':{'Away':'Panthers', 'Home':'Buccaneers','Conference':'NFC','TimeZone':'Eastern'},
    '108':{'Away':'Rams', 'Home':'Buccaneers','Conference':'NFC','TimeZone':'Eastern'},
    '109':{'Away':'Ravens', 'Home':'Buccaneers','Conference':'AFC','TimeZone':'Eastern'},
    '110':{'Away':'Saints', 'Home':'Buccaneers','Conference':'NFC','TimeZone':'Eastern'},
    '111':{'Away':'Vikings', 'Home':'Buccaneers','Conference':'NFC','TimeZone':'Eastern'},
    '112':{'Away':'Bills', 'Home':'Dolphins','Conference':'AFC','TimeZone':'Eastern'},
    '113':{'Away':'Chargers', 'Home':'Dolphins','Conference':'AFC','TimeZone':'Eastern'},
    '114':{'Away':'Chiefs', 'Home':'Dolphins','Conference':'AFC','TimeZone':'Eastern'},
    '115':{'Away':'Jets', 'Home':'Dolphins','Conference':'AFC','TimeZone':'Eastern'},
    '116':{'Away':'Packers', 'Home':'Dolphins','Conference':'NFC','TimeZone':'Eastern'},
    '117':{'Away':'Patriots', 'Home':'Dolphins','Conference':'AFC','TimeZone':'Eastern'},
    '118':{'Away':'Ravens', 'Home':'Dolphins','Conference':'AFC','TimeZone':'Eastern'},
    '119':{'Away':'Vikings', 'Home':'Dolphins','Conference':'NFC','TimeZone':'Eastern'},
    '120':{'Away':'Cowboys', 'Home':'Eagles','Conference':'NFC','TimeZone':'Eastern'},
    '121':{'Away':'Giants', 'Home':'Eagles','Conference':'NFC','TimeZone':'Eastern'},
    '122':{'Away':'Jaguars', 'Home':'Eagles','Conference':'AFC','TimeZone':'Eastern'},
    '123':{'Away':'Panthers', 'Home':'Eagles','Conference':'NFC','TimeZone':'Eastern'},
    '124':{'Away':'Rams', 'Home':'Eagles','Conference':'NFC','TimeZone':'Eastern'},
    '125':{'Away':'Redskins', 'Home':'Eagles','Conference':'NFC','TimeZone':'Eastern'},
    '126':{'Away':'Seahawks', 'Home':'Eagles','Conference':'NFC','TimeZone':'Eastern'},
    '127':{'Away':'Titans', 'Home':'Eagles','Conference':'AFC','TimeZone':'Eastern'},
    '128':{'Away':'Bears', 'Home':'Falcons','Conference':'NFC','TimeZone':'Eastern'},
    '129':{'Away':'Browns', 'Home':'Falcons','Conference':'AFC','TimeZone':'Eastern'},
    '130':{'Away':'Buccaneers', 'Home':'Falcons','Conference':'NFC','TimeZone':'Eastern'},
    '131':{'Away':'Cardinals', 'Home':'Falcons','Conference':'NFC','TimeZone':'Eastern'},
    '132':{'Away':'Lions', 'Home':'Falcons','Conference':'NFC','TimeZone':'Eastern'},
    '133':{'Away':'Panthers', 'Home':'Falcons','Conference':'NFC','TimeZone':'Eastern'},
    '134':{'Away':'Saints', 'Home':'Falcons','Conference':'NFC','TimeZone':'Eastern'},
    '135':{'Away':'Steelers', 'Home':'Falcons','Conference':'AFC','TimeZone':'Eastern'},
    '136':{'Away':'49ers', 'Home':'Giants','Conference':'NFC','TimeZone':'Eastern'},
    '137':{'Away':'Cardinals', 'Home':'Giants','Conference':'NFC','TimeZone':'Eastern'},
    '138':{'Away':'Colts', 'Home':'Giants','Conference':'AFC','TimeZone':'Eastern'},
    '139':{'Away':'Cowboys', 'Home':'Giants','Conference':'NFC','TimeZone':'Eastern'},
    '140':{'Away':'Eagles', 'Home':'Giants','Conference':'NFC','TimeZone':'Eastern'},
    '141':{'Away':'Falcons', 'Home':'Giants','Conference':'NFC','TimeZone':'Eastern'},
    '142':{'Away':'Redskins', 'Home':'Giants','Conference':'NFC','TimeZone':'Eastern'},
    '143':{'Away':'Texans', 'Home':'Giants','Conference':'AFC','TimeZone':'Eastern'},
    '144':{'Away':'Browns', 'Home':'Jaguars','Conference':'AFC','TimeZone':'Eastern'},
    '145':{'Away':'Colts', 'Home':'Jaguars','Conference':'AFC','TimeZone':'Eastern'},
    '146':{'Away':'Cowboys', 'Home':'Jaguars','Conference':'NFC','TimeZone':'Eastern'},
    '147':{'Away':'Dolphins', 'Home':'Jaguars','Conference':'AFC','TimeZone':'Eastern'},
    '148':{'Away':'Giants', 'Home':'Jaguars','Conference':'NFC','TimeZone':'Eastern'},
    '149':{'Away':'Steelers', 'Home':'Jaguars','Conference':'AFC','TimeZone':'Eastern'},
    '150':{'Away':'Texans', 'Home':'Jaguars','Conference':'AFC','TimeZone':'Eastern'},
    '151':{'Away':'Titans', 'Home':'Jaguars','Conference':'AFC','TimeZone':'Eastern'},
    '152':{'Away':'Bears', 'Home':'Jets','Conference':'NFC','TimeZone':'Eastern'},
    '153':{'Away':'Bills', 'Home':'Jets','Conference':'AFC','TimeZone':'Eastern'},
    '154':{'Away':'Broncos', 'Home':'Jets','Conference':'AFC','TimeZone':'Eastern'},
    '155':{'Away':'Dolphins', 'Home':'Jets','Conference':'AFC','TimeZone':'Eastern'},
    '156':{'Away':'Lions', 'Home':'Jets','Conference':'NFC','TimeZone':'Eastern'},
    '157':{'Away':'Patriots', 'Home':'Jets','Conference':'AFC','TimeZone':'Eastern'},
    '158':{'Away':'Raiders', 'Home':'Jets','Conference':'AFC','TimeZone':'Eastern'},
    '159':{'Away':'Steelers', 'Home':'Jets','Conference':'AFC','TimeZone':'Eastern'},
    '160':{'Away':'Bears', 'Home':'Lions','Conference':'NFC','TimeZone':'Eastern'},
    '161':{'Away':'Bills', 'Home':'Lions','Conference':'AFC','TimeZone':'Eastern'},
    '162':{'Away':'Buccaneers', 'Home':'Lions','Conference':'NFC','TimeZone':'Eastern'},
    '163':{'Away':'Dolphins', 'Home':'Lions','Conference':'AFC','TimeZone':'Eastern'},
    '164':{'Away':'Giants', 'Home':'Lions','Conference':'NFC','TimeZone':'Eastern'},
    '165':{'Away':'Packers', 'Home':'Lions','Conference':'NFC','TimeZone':'Eastern'},
    '166':{'Away':'Saints', 'Home':'Lions','Conference':'NFC','TimeZone':'Eastern'},
    '167':{'Away':'Vikings', 'Home':'Lions','Conference':'NFC','TimeZone':'Eastern'},
    '168':{'Away':'Bears', 'Home':'Panthers','Conference':'NFC','TimeZone':'Eastern'},
    '169':{'Away':'Browns', 'Home':'Panthers','Conference':'AFC','TimeZone':'Eastern'},
    '170':{'Away':'Buccaneers', 'Home':'Panthers','Conference':'NFC','TimeZone':'Eastern'},
    '171':{'Away':'Falcons', 'Home':'Panthers','Conference':'NFC','TimeZone':'Eastern'},
    '172':{'Away':'Lions', 'Home':'Panthers','Conference':'NFC','TimeZone':'Eastern'},
    '173':{'Away':'Saints', 'Home':'Panthers','Conference':'NFC','TimeZone':'Eastern'},
    '174':{'Away':'Seahawks', 'Home':'Panthers','Conference':'NFC','TimeZone':'Eastern'},
    '175':{'Away':'Steelers', 'Home':'Panthers','Conference':'AFC','TimeZone':'Eastern'},
    '176':{'Away':'Bears', 'Home':'Patriots','Conference':'NFC','TimeZone':'Eastern'},
    '177':{'Away':'Bengals', 'Home':'Patriots','Conference':'AFC','TimeZone':'Eastern'},
    '178':{'Away':'Bills', 'Home':'Patriots','Conference':'AFC','TimeZone':'Eastern'},
    '179':{'Away':'Broncos', 'Home':'Patriots','Conference':'AFC','TimeZone':'Eastern'},
    '180':{'Away':'Dolphins', 'Home':'Patriots','Conference':'AFC','TimeZone':'Eastern'},
    '181':{'Away':'Jets', 'Home':'Patriots','Conference':'AFC','TimeZone':'Eastern'},
    '182':{'Away':'Lions', 'Home':'Patriots','Conference':'NFC','TimeZone':'Eastern'},
    '183':{'Away':'Raiders', 'Home':'Patriots','Conference':'AFC','TimeZone':'Eastern'},
    '184':{'Away':'Bengals', 'Home':'Ravens','Conference':'AFC','TimeZone':'Eastern'},
    '185':{'Away':'Browns', 'Home':'Ravens','Conference':'AFC','TimeZone':'Eastern'},
    '186':{'Away':'Chargers', 'Home':'Ravens','Conference':'AFC','TimeZone':'Eastern'},
    '187':{'Away':'Falcons', 'Home':'Ravens','Conference':'NFC','TimeZone':'Eastern'},
    '188':{'Away':'Jaguars', 'Home':'Ravens','Conference':'AFC','TimeZone':'Eastern'},
    '189':{'Away':'Panthers', 'Home':'Ravens','Conference':'NFC','TimeZone':'Eastern'},
    '190':{'Away':'Steelers', 'Home':'Ravens','Conference':'AFC','TimeZone':'Eastern'},
    '191':{'Away':'Titans', 'Home':'Ravens','Conference':'AFC','TimeZone':'Eastern'},
    '192':{'Away':'Buccaneers', 'Home':'Redskins','Conference':'NFC','TimeZone':'Eastern'},
    '193':{'Away':'Cowboys', 'Home':'Redskins','Conference':'NFC','TimeZone':'Eastern'},
    '194':{'Away':'Eagles', 'Home':'Redskins','Conference':'NFC','TimeZone':'Eastern'},
    '195':{'Away':'Giants', 'Home':'Redskins','Conference':'NFC','TimeZone':'Eastern'},
    '196':{'Away':'Jaguars', 'Home':'Redskins','Conference':'AFC','TimeZone':'Eastern'},
    '197':{'Away':'Rams', 'Home':'Redskins','Conference':'NFC','TimeZone':'Eastern'},
    '198':{'Away':'Seahawks', 'Home':'Redskins','Conference':'NFC','TimeZone':'Eastern'},
    '199':{'Away':'Titans', 'Home':'Redskins','Conference':'AFC','TimeZone':'Eastern'},
    '200':{'Away':'Bengals', 'Home':'Steelers','Conference':'AFC','TimeZone':'Eastern'},
    '201':{'Away':'Browns', 'Home':'Steelers','Conference':'AFC','TimeZone':'Eastern'},
    '202':{'Away':'Buccaneers', 'Home':'Steelers','Conference':'NFC','TimeZone':'Eastern'},
    '203':{'Away':'Chiefs', 'Home':'Steelers','Conference':'AFC','TimeZone':'Eastern'},
    '204':{'Away':'Colts', 'Home':'Steelers','Conference':'AFC','TimeZone':'Eastern'},
    '205':{'Away':'Ravens', 'Home':'Steelers','Conference':'AFC','TimeZone':'Eastern'},
    '206':{'Away':'Saints', 'Home':'Steelers','Conference':'NFC','TimeZone':'Eastern'},
    '207':{'Away':'Texans', 'Home':'Steelers','Conference':'AFC','TimeZone':'Eastern'},
    '208':{'Away':'49ers', 'Home':'Broncos','Conference':'NFC','TimeZone':'Mountain'},
    '209':{'Away':'Bills', 'Home':'Broncos','Conference':'AFC','TimeZone':'Mountain'},
    '210':{'Away':'Cardinals', 'Home':'Broncos','Conference':'NFC','TimeZone':'Mountain'},
    '211':{'Away':'Chargers', 'Home':'Broncos','Conference':'AFC','TimeZone':'Mountain'},
    '212':{'Away':'Chiefs', 'Home':'Broncos','Conference':'AFC','TimeZone':'Mountain'},
    '213':{'Away':'Colts', 'Home':'Broncos','Conference':'AFC','TimeZone':'Mountain'},
    '214':{'Away':'Dolphins', 'Home':'Broncos','Conference':'AFC','TimeZone':'Mountain'},
    '215':{'Away':'Raiders', 'Home':'Broncos','Conference':'AFC','TimeZone':'Mountain'},
    '216':{'Away':'49ers', 'Home':'Cardinals','Conference':'NFC','TimeZone':'Mountain'},
    '217':{'Away':'Chargers', 'Home':'Cardinals','Conference':'AFC','TimeZone':'Mountain'},
    '218':{'Away':'Chiefs', 'Home':'Cardinals','Conference':'AFC','TimeZone':'Mountain'},
    '219':{'Away':'Eagles', 'Home':'Cardinals','Conference':'NFC','TimeZone':'Mountain'},
    '220':{'Away':'Lions', 'Home':'Cardinals','Conference':'NFC','TimeZone':'Mountain'},
    '221':{'Away':'Rams', 'Home':'Cardinals','Conference':'NFC','TimeZone':'Mountain'},
    '222':{'Away':'Redskins', 'Home':'Cardinals','Conference':'NFC','TimeZone':'Mountain'},
    '223':{'Away':'Seahawks', 'Home':'Cardinals','Conference':'NFC','TimeZone':'Mountain'},
    '224':{'Away':'Bears', 'Home':'49ers','Conference':'NFC','TimeZone':'Pacific'},
    '225':{'Away':'Cardinals', 'Home':'49ers','Conference':'NFC','TimeZone':'Pacific'},
    '226':{'Away':'Chargers', 'Home':'49ers','Conference':'AFC','TimeZone':'Pacific'},
    '227':{'Away':'Chiefs', 'Home':'49ers','Conference':'AFC','TimeZone':'Pacific'},
    '228':{'Away':'Eagles', 'Home':'49ers','Conference':'NFC','TimeZone':'Pacific'},
    '229':{'Away':'Rams', 'Home':'49ers','Conference':'NFC','TimeZone':'Pacific'},
    '230':{'Away':'Redskins', 'Home':'49ers','Conference':'NFC','TimeZone':'Pacific'},
    '231':{'Away':'Seahawks', 'Home':'49ers','Conference':'NFC','TimeZone':'Pacific'},
    '232':{'Away':'Broncos', 'Home':'Chargers','Conference':'AFC','TimeZone':'Pacific'},
    '233':{'Away':'Chiefs', 'Home':'Chargers','Conference':'AFC','TimeZone':'Pacific'},
    '234':{'Away':'Jaguars', 'Home':'Chargers','Conference':'AFC','TimeZone':'Pacific'},
    '235':{'Away':'Jets', 'Home':'Chargers','Conference':'AFC','TimeZone':'Pacific'},
    '236':{'Away':'Patriots', 'Home':'Chargers','Conference':'AFC','TimeZone':'Pacific'},
    '237':{'Away':'Raiders', 'Home':'Chargers','Conference':'AFC','TimeZone':'Pacific'},
    '238':{'Away':'Rams', 'Home':'Chargers','Conference':'NFC','TimeZone':'Pacific'},
    '239':{'Away':'Seahawks', 'Home':'Chargers','Conference':'NFC','TimeZone':'Pacific'},
    '240':{'Away':'49ers', 'Home':'Raiders','Conference':'NFC','TimeZone':'Pacific'},
    '241':{'Away':'Bills', 'Home':'Raiders','Conference':'AFC','TimeZone':'Pacific'},
    '242':{'Away':'Broncos', 'Home':'Raiders','Conference':'AFC','TimeZone':'Pacific'},
    '243':{'Away':'Cardinals', 'Home':'Raiders','Conference':'NFC','TimeZone':'Pacific'},
    '244':{'Away':'Chargers', 'Home':'Raiders','Conference':'AFC','TimeZone':'Pacific'},
    '245':{'Away':'Chiefs', 'Home':'Raiders','Conference':'AFC','TimeZone':'Pacific'},
    '246':{'Away':'Dolphins', 'Home':'Raiders','Conference':'AFC','TimeZone':'Pacific'},
    '247':{'Away':'Texans', 'Home':'Raiders','Conference':'AFC','TimeZone':'Pacific'},
    '248':{'Away':'49ers', 'Home':'Seahawks','Conference':'NFC','TimeZone':'Pacific'},
    '249':{'Away':'Broncos', 'Home':'Seahawks','Conference':'AFC','TimeZone':'Pacific'},
    '250':{'Away':'Cardinals', 'Home':'Seahawks','Conference':'NFC','TimeZone':'Pacific'},
    '251':{'Away':'Cowboys', 'Home':'Seahawks','Conference':'NFC','TimeZone':'Pacific'},
    '252':{'Away':'Giants', 'Home':'Seahawks','Conference':'NFC','TimeZone':'Pacific'},
    '253':{'Away':'Packers', 'Home':'Seahawks','Conference':'NFC','TimeZone':'Pacific'},
    '254':{'Away':'Raiders', 'Home':'Seahawks','Conference':'AFC','TimeZone':'Pacific'},
    '255':{'Away':'Rams', 'Home':'Seahawks','Conference':'NFC','TimeZone':'Pacific'},    
}

# This value is used to determine the size of the board when doing an n-queens problem
GRIDSIZE = 8

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
VARIABLE_ORDERING = False

class CSPFeature:
    def __init__(self, strName, lstDomain):
        """
        Create a feature object, which represents a feature/variable in the CSP graph.
        Set the name and domain of the feature. The value starts out as unassigned.
        """
        # assign the name of the feature represented by the node
        self.name = str(strName)
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
        elif (strConstraint == "NotEqualHomeAway"):
            # create a new constraint object from tail to head
            newConstraint = CSPConstraintNotEqualHomeAway(self.getFeature(ftrTail), strConstraint, self.getFeature(ftrHead))
            # put the new constraint in the graph's list of constraints
            self.constraints.append(newConstraint)
            # create a new constraint object from head to tail
            newConstraint = CSPConstraintNotEqualHomeAway(self.getFeature(ftrHead), strConstraint, self.getFeature(ftrTail))
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
            if (len(constraintList) % 10 == 0):
                print "\tconsistency checking constraints = " + str(len(constraintList))
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
    print "Backtracking feature index = " + str(featureIndex)
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


class CSPConstraintNotEqualHomeAway(CSPConstraint):
    def __init__(self, ftrTail, strConstraint, ftrHead):
        # call the parent constructor
        CSPConstraint.__init__(self, ftrTail, strConstraint, ftrHead)

    def satisfied(self, tailValue, headValue):
        """
        returns false if head and tail features (which represent NFL games) have the same
        home or away team and true if they have different values or one of the features
        does not have a value
        """
        # access table of nfl games
        global nflGames
        # if the head or the tail haven't been assigned, then the constraint is satisfied
        if headValue == "none" or tailValue == "none":
            return True
        # compare the home teams for the two games
        home1 = nflGames[str(tailValue)]['Home']
        home2 = nflGames[str(headValue)]['Home']
        away1 = nflGames[str(tailValue)]['Away']
        away2 = nflGames[str(headValue)]['Away']
        if (home1 == home2 or home1 == away1 or home1 == away2):
            return False
        # compare the away teams for the two games
        if (home2 == away1 or home2 == away2 or away1 == away2):
            return False
        # otherwise, they are different so the constraint is satisfied
        return True




def NFLSchedule():
    global NUMBER_OF_WEEKS
    global GAMES_PER_WEEK
    # create a csp graph
    cspGraph = CSPGraph()

    # add a feature for each position in the schedule
    # within a week:
    # game 0 = Thursday
    # games 1-11 = Sunday afternoon
    # games 12-15 = Sunday evening, Sunday night, Monday night
    print "1"
    for schedulePosition in range(0, NUMBER_OF_WEEKS*GAMES_PER_WEEK):
        #cspGraph.addFeature(schedulePosition, range(0, NUMBER_OF_WEEKS*GAMES_PER_WEEK))
        cspGraph.addFeature(schedulePosition, range(0, 256))

    # Each game gets played only once, so all features have a "not equal" constraint with the other features
    print "2"
    for position1 in range(0, NUMBER_OF_WEEKS*GAMES_PER_WEEK):
        for position2 in range(position1+1, NUMBER_OF_WEEKS*GAMES_PER_WEEK):
            cspGraph.addConstraint(str(position1), '!=', str(position2))

    # Each team plays exactly one thursday game - that means that the home and away teams for each
    # game on Thursday have to be different
    print "3"
    for firstThursday in range(0, NUMBER_OF_WEEKS*GAMES_PER_WEEK, NUMBER_OF_WEEKS):
        for secondThursday in range (firstThursday+GAMES_PER_WEEK, NUMBER_OF_WEEKS*GAMES_PER_WEEK, GAMES_PER_WEEK):
            cspGraph.addConstraint(str(firstThursday), 'NotEqualHomeAway', str(secondThursday))

    # Each team plays one game each week - that means the home and away teams for each game within each week
    # have to be different
    print "4"
    for week in range(0, NUMBER_OF_WEEKS):
        for firstPosition in range(0, GAMES_PER_WEEK):
            for secondPosition in range(firstPosition+1, GAMES_PER_WEEK):
                pos1 = week * GAMES_PER_WEEK + firstPosition
                pos2 = week * GAMES_PER_WEEK + secondPosition
                cspGraph.addConstraint(str(pos1), 'NotEqualHomeAway', str(pos2))

    # call backtracking search
    print "starting backtracking..."
    backtrackingSearch(cspGraph, 0)




#NQueens()
#MapColoring()
NFLSchedule()