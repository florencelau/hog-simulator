"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    outcomes_list = [] #list for dice outcomes to check for 1's
    counter = 1 
    while counter <= num_rolls:
        outcomes_list.append(dice()) #adds numbers from dice() into outcomes_list
        counter += 1
    if 1 in outcomes_list:
        return 0
    else:
        return sum(outcomes_list)
    #END Question 1

def is_prime(total):
    """If total turn score is prime, return True. If not, return False.

    >>> is_prime(16)
    False
    >>> is_prime(0)
    False
    >>> is_prime(3)
    True
    """
    if total == 0 or total == 1:
        return False 
    counter = 2   
    while counter < total: 
        if total % counter == 0: 
           return False
        else:
            counter += 1
    return True

def next_prime(total):
    """Find the next prime number after that of is_prime()

    >>> next_prime(5)
    7 
    >>> next_prime(30)
    31
    """
    counter = 1
    while counter <= total:
        if is_prime(total + counter) == False:
            counter += 1
        else:
            return total + counter
    

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls > 0:
        # HOGTIMUS PRIME
        normal_roll = roll_dice(num_rolls, dice)
        if is_prime(normal_roll):
            return next_prime(normal_roll)
        # NORMAL TURN
        else: 
            return normal_roll
    else:
        # FREE BACON, if num_rolls is 0 
        x = opponent_score % 10 
        y = opponent_score // 10
        normal_roll = 1 + max(x, y)
        if is_prime(normal_roll):
            return next_prime(normal_roll)
        else:
            return normal_roll
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 != 0: 
        return six_sided
    else: 
        return four_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    me_first = score0 // 10 
    opp_first = score1 // 10
    me_second = score0 % 10
    opp_second = score1 % 10 

    if score0 > 100:
        me_first = (score0 - 100) // 10
    if score1 > 100: 
        opp_first = (score1 - 100) // 10
    if me_first == opp_second and opp_first == me_second:
        return True
    else:
        return False
    # END Question 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    
    # BEGIN Question 5
    while score0 < goal and score1 < goal:
        dice = select_dice(score0, score1)
        rollzero = strategy0(score0, score1)
        rollone = strategy1(score1, score0)
        if player == 0:
            turn = take_turn(rollzero, score1, dice)
            if turn == 0:
                score1 = score1 + rollzero
            else: 
                score0 = score0 + turn
        if player == 1:
            turn = take_turn(rollone, score0, dice)
            if turn == 0: 
                score0 = score0 + rollone
            else: 
                score1 = score1 + turn
        if is_swap(score0, score1): 
            score0, score1 = score1, score0
        player = other(player)
    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def averaged(*args):
        counter = 1
        result = 0
        while counter <= num_samples:
            counter += 1
            result = result + fn(*args)
        return result / num_samples
    return averaged 
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    num_rolls = 1
    list_of_averages = [] 
    while num_rolls <= 10: 
        each_average = make_averaged(roll_dice, num_samples)(num_rolls, dice) #do not add parameters to roll_dice
        list_of_averages.append(each_average)
        num_rolls += 1
    return list_of_averages.index(max(list_of_averages)) + 1 
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
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
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:
        print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    opp_first = opponent_score // 10
    opp_second = opponent_score % 10 
    the_opp_max = max(opp_first, opp_second) + 1
    if is_prime(the_opp_max): 
        the_opp_max = next_prime(the_opp_max)
    if the_opp_max >= margin:
        return 0
    else: 
        return num_rolls
    # END Question 8

def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    opp_first = opponent_score // 10 
    opp_second = opponent_score % 10
    the_opp_max = max(opp_first, opp_second)+1
    if is_prime(the_opp_max):
        the_opp_max = next_prime(the_opp_max) 
    if score + the_opp_max == (opp_second * 10) + opp_first:
        new_score = score + the_opp_max
        if opponent_score > new_score:
            return 0 
    return num_rolls
    # END Question 9


def final_strategy(score, opponent_score):
    """This strategy returns the optimal times to roll considering both bacon_strategy
    and swap_strategy... 
    """ 
    # BEGIN Question 10 
    opp_first = opponent_score // 10 
    opp_second = opponent_score % 10
    me_first = score // 10
    me_second = score % 10 
    the_opp_max = max(opp_first, opp_second) + 1
    dice = select_dice(score, opponent_score)
    # roll_dice(num_rolls, dice)
    # take_turn(num_rolls, opponent_score, dice)

    #avoid rolling a 1
    #try to get to a prime number while preventing opponent from getting a beneficial swap
    #skip turn if 

    num_rolls = 10
    if me_first < me_second:
        while num_rolls > 1: 
            temp_score = opponent_score + num_rolls 
            if is_swap(score, temp_score):
                return num_rolls
            if dice == four_sided and num_rolls < 5:
                temp_score = opponent_score + num_rolls
                if is_swap(score, temp_score):
                    return num_rolls 
            num_rolls -= 1 
    # if opponent_score > score:
    #     wanted_score = int(str(opp_second) + str(opp_first)) 
    #     optimal_turn_score = wanted_score - score
    #     return abs(optimal_turn_score)
    #     # if optimal_turn_score == 1 and the_opp_max >= 2:
    #     #     return 0
    # else:
    #     score_to_avoid = opponent_score - int(str(me_second) + str(me_first))
    #     return abs(score_to_avoid) + 1
    #     # if score_to_avoid == 1 and the_opp_max >= 2:
    #     #     return 0
    if is_prime(the_opp_max + score) == True:
        return 0
    if is_prime(the_opp_max):
        the_opp_max = next_prime(the_opp_max)
    # If my score is close to 100, I want to roll 0 here if free bacon gets me >= 100
    if the_opp_max + score >= 100:
        if not is_swap(the_opp_max + score, opponent_score): 
            return 0 

    if is_swap(score, opponent_score) == False:
        if opponent_score > score:
            wanted_score = int(str(me_second) + str(me_first)) 
            optimal_turn_score = wanted_score - opponent_score
            if optimal_turn_score in range(11):
                return optimal_turn_score

    hypothetical_score = score + the_opp_max 
    if is_swap(hypothetical_score, opponent_score):
        return 0

    #if free bacon is beneficial
    if bacon_strategy(score, opponent_score, margin = 6) == 0:
        return 0

    #if swap is beneficial
    if swap_strategy(score, opponent_score) == 0:
        return 0 

    #try to prevent switching to a four_sided dice (hog wild)
    counter = 1
    while counter <= 6: 
        score += counter
        counter += 1
        if (score + opponent_score) % 7 == 0:
            counter = 7
            return 0
    while is_swap(score, opponent_score) == False and counter < 10: 
        opponent_score += counter
        counter += 1
    return counter

    # while opponent_score > score:
    #     score + opponent_score
    # possible_score = 
    # if 
    if the_opp_max == (100 - score):
        return 0
    if dice == six_sided:
        num_rolls = 4 
        if score > 97: 
            num_rolls = 1
        if score > 95:
            num_rolls = 2
        if score > 94:
            num_rolls = 3
    else: 
        num_rolls = 3
        if score > 98: 
            num_rolls = 1
        if score > 97:
            num_rolls = 2
    if dice == four_sided:
        return 0
    return num_rolls
    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


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
