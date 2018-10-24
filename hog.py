"""The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    sumOfOutcomes = 0
    check = False
    for i in range(num_rolls):
        num = dice()
        if(num == 1):
            sumOfOutcomes = 1
            check = True
        elif(not check):
            sumOfOutcomes += num 
    return sumOfOutcomes


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    tens = score // 10
    ones = score % 10
    points = 2*tens - ones
    return points if points > 1 else 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls,dice)


def is_swap(player_score, opponent_score):
    """
    Return whether the current player's score has the same absolute
    difference between its last two digits as the opponent's score.
    """
    playerLastTwo =  player_score % 100
    opponentLastTwo = opponent_score % 100
    playerTens = playerLastTwo // 10
    playerOnes = playerLastTwo % 10
    opponentTens = opponentLastTwo // 10
    opponentOnes = opponentLastTwo % 10
    return True if abs(playerTens - playerOnes) == abs(opponentTens - opponentOnes) else False


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    return silence

def swaps(player_score,opponent_score):

    return (opponent_score, player_score) if is_swap(player_score,opponent_score) else (player_score,opponent_score)

def pointsAdd(player_score, opponent_score, strategy, dice):
     num_rolls = strategy(player_score,opponent_score)
     player_score += take_turn(num_rolls, opponent_score,dice)
     return swaps(player_score,opponent_score)

def average(n=1000):
    turns = {}
    for i in range(100):
        turns[i] =0
    for i in range(n):
        playerZeroScore, playerOneScore, tempturn = play(final_strategy, final_strategy,goal=100)
        for key in tempturn:
            turns[key] = tempturn[key] + turns[key]
    for key in turns:
        print(turns[key]//1000)
def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    turns = {}
    turn = 1
    while(score1 < goal and score0 < goal):

        if(player == 0 ):
            score0, score1 = pointsAdd(score0,score1,strategy0,dice)
            player = other(player)
            turns[turn] = score0
        elif(player == 1):
            score1, score0 = pointsAdd(score1,score0,strategy1,dice)
            player = other(player)
            turns[turn] = score1
        say = say(score0,score1)
        turn +=1

    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(previous_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != previous_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 18) # Player 0 gets 8 points, then Swine Swap applies
    Player 0 now has 6 and Player 1 now has 18
    Player 1 takes the lead by 12
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, previous_high=0, previous_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(11, 0)
    >>> f2 = f1(11, 9)
    9 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 9)
    >>> f4 = f3(12, 20) # Player 1 gets 3 points, then Swine Swap applies
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f5 = f4(20, 32) # Player 0 gets 20 points, then Swine Swap applies
    12 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 42) # Player 1 gets 10 points; not enough for a new high
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'

    def say(score0, score1):
        if(who):
            current_score = score1
        else:
            current_score = score0 
        temp_value = current_score - previous_score
        highest = previous_high
        if(temp_value > highest):
                highest = temp_value
                print(temp_value, "point(s)! That's the biggest gain yet for Player", who)
        return(announce_highest(who,highest,current_score))
    return say


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    assert num_samples!=0,'num_samples is 0'
    def function_call(*args):
        value = 0
        for i in range(num_samples):
            value += fn(*args)
        return value / num_samples
    return function_call


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    minRolls = 0
    maxScore = 0
    average = make_averaged(roll_dice, num_samples)
    for i in range(1,11):
        score = average(i,dice)
        if score > maxScore:
            maxScore = score
            minRolls = i
    return minRolls



def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    return 0 if free_bacon(opponent_score) >= margin else num_rolls  # Replace this statement


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
    """
    scoreAdded = free_bacon(opponent_score)
    newScore = score +scoreAdded
    if(newScore < opponent_score and is_swap(newScore,opponent_score)):
        return 0
    if(scoreAdded >= margin):
        if(newScore >= opponent_score and is_swap(newScore,opponent_score)):
            return num_rolls
        return 0
    return  num_rolls


def final_strategy(score, opponent_score, dice=six_sided):
    return 1


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()