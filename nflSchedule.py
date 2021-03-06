__author__ = 'rsimpson'


from constraintSatisfaction import *

# how many weeks in the season?
NUMBER_OF_WEEKS = 16

# how many games per week?
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


class CSPGraphNFL(CSPGraph):
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


def NFLSchedule():
    global NUMBER_OF_WEEKS
    global GAMES_PER_WEEK
    global nflGames
    # create a csp graph
    cspGraph = CSPGraphNFL()

    # make a list to store the indices for all the Thursday games
    thursdayGames = []
    # make a list to store the indices for all the Monday games
    mondayGames = []
    # make a list to store the indices for all the afternoon games (when only eastern and central teams play)
    afternoonGames = []
    # make a list to store the indices for all the evening games (when any team can play
    eveningGames = []
    # fill in values for the lists
    for week in range(0, NUMBER_OF_WEEKS):
        # each week, game 0 = Thursday
        thursdayGames.append(week * GAMES_PER_WEEK)
        # each week, game 15 = Monday
        mondayGames.append((week * GAMES_PER_WEEK) + (GAMES_PER_WEEK - 1))
        # each week, games 1-11 = Sunday afternoon
        for game in range(1,12):
            afternoonGames.append((week * GAMES_PER_WEEK) + game)
        # each week, games 0, 12-15 = evening games
        eveningGames.append(week * GAMES_PER_WEEK)
        for game in range(12,16):
            eveningGames.append((week * GAMES_PER_WEEK) + game)

    # make a list to store all the east/central time zone games
    eastCentralGames = []
    # make a list to store all the mountain/pacific time zone games
    mountainPacificGames = []
    # fill in the values for the lists
    for game in range(0, NUMBER_OF_WEEKS * GAMES_PER_WEEK):
        if nflGames[str(game)]['TimeZone'] == 'Eastern' or nflGames[str(game)]['TimeZone'] == 'Central':
            eastCentralGames.append(game)
        elif nflGames[str(game)]['TimeZone'] == 'Mountain' or nflGames[str(game)]['TimeZone'] == 'Pacific':
            mountainPacificGames.append(game)
        else:
            print "ERROR: I got a bad time zone!"
            exit()

    # add a feature for each position in the schedule within a week:
    print "Adding features..."
    # the first game (slot 0) is always a home game for the super bowl champion - in this case,
    # the seattle seahawks
    cspGraph.addFeature(0, range(248, 256))
    # fill in the rest of the games
    for schedulePosition in range(1, NUMBER_OF_WEEKS*GAMES_PER_WEEK):
        # afternoon slots can only hold east and central cost games
        if schedulePosition in afternoonGames:
            cspGraph.addFeature(schedulePosition, eastCentralGames)
        # evening slots can hold any game
        elif schedulePosition in eveningGames:
            cspGraph.addFeature(schedulePosition, range(0, NUMBER_OF_WEEKS*GAMES_PER_WEEK))

    # Each game gets played only once, so all features have a "not equal" constraint with the other features
    print "Adding constraint - not equal constraint between all features..."
    for position1 in range(0, NUMBER_OF_WEEKS*GAMES_PER_WEEK):
        for position2 in range(position1+1, NUMBER_OF_WEEKS*GAMES_PER_WEEK):
            ftrTail = str(position1)
            ftrHead = str(position2)
            strConstraint = 'NotEqual'
            # create a new constraint object from tail to head
            newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrTail), strConstraint, cspGraph.getFeature(ftrHead))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)
            # create a new constraint object from head to tail
            newConstraint = CSPConstraintNotEqual(cspGraph.getFeature(ftrHead), strConstraint, cspGraph.getFeature(ftrTail))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)

    # Each team plays exactly one thursday game - that means that the home and away teams for each
    # game on Thursday have to be different
    print "Adding constraint - each team plays a Thursday game..."
    for firstThursday in range(0, NUMBER_OF_WEEKS*GAMES_PER_WEEK, NUMBER_OF_WEEKS):
        for secondThursday in range (firstThursday+GAMES_PER_WEEK, NUMBER_OF_WEEKS*GAMES_PER_WEEK, GAMES_PER_WEEK):
            ftrTail = str(firstThursday)
            ftrHead = str(secondThursday)
            strConstraint = 'NotEqualHomeAway'
            # create a new constraint object from tail to head
            newConstraint = CSPConstraintNotEqualHomeAway(cspGraph.getFeature(ftrTail), strConstraint, cspGraph.getFeature(ftrHead))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)
            # create a new constraint object from head to tail
            newConstraint = CSPConstraintNotEqualHomeAway(cspGraph.getFeature(ftrHead), strConstraint, cspGraph.getFeature(ftrTail))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)

    # Teams who played on Monday don't play their next game on Thursday
    print "Adding constraint - no team plays a Thursday game after a Monday game..."
    for mondayGame in mondayGames:
        for thursdayGame in thursdayGames:
            ftrTail = str(mondayGame)
            ftrHead = str(thursdayGame)
            strConstraint = 'NotEqualHomeAway'
            # create a new constraint object from tail to head
            newConstraint = CSPConstraintNotEqualHomeAway(cspGraph.getFeature(ftrTail), strConstraint, cspGraph.getFeature(ftrHead))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)
            # create a new constraint object from head to tail
            newConstraint = CSPConstraintNotEqualHomeAway(cspGraph.getFeature(ftrHead), strConstraint, cspGraph.getFeature(ftrTail))
            # put the new constraint in the graph's list of constraints
            cspGraph.constraints.append(newConstraint)

    # Each team plays one game each week - that means the home and away teams for each game within each week
    # have to be different
    print "Adding constraint - no team plays more than one game per week..."
    for week in range(0, NUMBER_OF_WEEKS):
        for firstPosition in range(0, GAMES_PER_WEEK):
            for secondPosition in range(firstPosition+1, GAMES_PER_WEEK):
                pos1 = week * GAMES_PER_WEEK + firstPosition
                pos2 = week * GAMES_PER_WEEK + secondPosition
                ftrTail = str(pos1)
                ftrHead = str(pos2)
                strConstraint = 'NotEqualHomeAway'
                # create a new constraint object from tail to head
                newConstraint = CSPConstraintNotEqualHomeAway(cspGraph.getFeature(ftrTail), strConstraint, cspGraph.getFeature(ftrHead))
                # put the new constraint in the graph's list of constraints
                cspGraph.constraints.append(newConstraint)
                # create a new constraint object from head to tail
                newConstraint = CSPConstraintNotEqualHomeAway(cspGraph.getFeature(ftrHead), strConstraint, cspGraph.getFeature(ftrTail))
                # put the new constraint in the graph's list of constraints
                cspGraph.constraints.append(newConstraint)

    # call backtracking search
    print "starting backtracking..."
    backtrackingSearch(cspGraph, 0)

    #print "starting hill climbing"
    #hillClimbingSearch(cspGraph)


NFLSchedule()
