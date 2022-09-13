import random
import math

# STARTING_VALUE determines the original mixed strategy set. For example, a value of 25 results in a strategy of
# [25, 25, 25]. Higher values make the algorithm converge slower, but are more stable and resistant to effects such as
# extinction (any choice hitting 0, causing anything it beats to become dominant).
# As long as STARTING_VALUE * 100 < ITERATIONS * EPOCHS, you should have no problem getting the algorithm to converge.
STARTING_VALUE = 10000

# DETERRENT is how much the losing side is punished, which is then multiplied by the reward for the winning side.
# For instance, if paper (+5) wins and DETERRENT = -.4, then paper is rewarded +5 and rock is punished -2.
# Warning that values lower than -1 will result in a negative-sum game, leading to extinction.
# Should be kept between -1 and 0 for sustainability.
DETERRENT = -1

# LOSE, TIE, and WIN are set to arbitrary values so it makes more sense when I type "if result == LOSE" or something.
# The actual numbers attached to them don't do anything.
LOSE = 0
TIE = 1
WIN = 2

# SIZE is the amount of choices in the game. For example, SIZE = 3 produces classic rock-paper-scissors, while
# SIZE = 5 produces RPS with five possible moves.
# Only positive odd numbers produce a balanced game.
SIZE = 3

# REWARDS is the weighting for the game. For example, REWARDS = [3, 2, 1] gives +3 if you win with rock, +2 if you
# win with paper, +1 if you win with scissors.
# The length of this array must be equal to SIZE.
REWARDS = [2, 1, 1]

# TIE_REWARDS can be used if you want to benefit or punish ties. It works the same way as REWARDS.
# Note that any values here will be applied twice, because the same choice was used by both sides.
# For example, if rock gets +1 for a tie, then a rock tie will result in +2 for rock.
TIE_REWARDS = [0, 0, 0]

# ITERATIONS is the number of games simulated per epoch.
ITERATIONS = 6000

# EPOCHS is the number of epochs simulated. Epochs are like groups of iterations. After each one, the program will
# print out some stats so you can see how the model progresses over time. I recommend 10-20 epochs if you're looking
# over the stats manually, but I used 50 for the graphs.
EPOCHS = 500

STATCOMBINE_BASE = 0
STATCOMBINE_EXP = 5


def convert_coords_to_triangle(r, p, s):
    r3 = math.sqrt(3) / 6
    return [-p / 2 + s / 2, 2*r3 * r - r3 * p - r3 * s + r3]


def convert_triangle_to_coords(x, y):
    p = y / math.sqrt(3)
    return [2*p, -x - p + 1/2, x - p + 1/2]


def rotate(x1, y1, angle):
    x2 = x1 * math.cos(angle) - y1 * math.sin(angle)
    y2 = x1 * math.sin(angle) + y1 * math.cos(angle)
    return [x2, y2]


def normalize(array, product=1):
    sum = 0
    return_array = []
    for item in array:
        sum += abs(item)
    for item in array:
        return_array.append(item * product / sum)
    return return_array


def vector_to_angle(x, y):
    hypotenuse = math.sqrt(x ** 2 + y ** 2)
    if x > 0:
        return math.asin(y / hypotenuse)
    else:
        return math.pi - math.asin(y / hypotenuse)


def subtract_array(array1, array2):
    array3 = []
    for item in range(len(array1)):
        array3.append(array1[item] - array2[item])
    return array3


def add_array(array1, array2):
    array3 = []
    for item in range(len(array1)):
        array3.append(array1[item] + array2[item])
    return array3


def decide_game(a, b, size):
    # Simulates an rps-x game between two choices, a and b.
    # a and b are player choices, must be between 0 and size-1.
    # size is the size of the game; for example, 5 gives rps-5 (5 elements). size must be odd.
    # Returns WIN if a wins, LOSE if b wins, TIE if a and b pick the same choice.
    if a == b:
        return TIE
    # In rps-101, choice 50 will beat 0-49, but lose to 51-100.
    # Choice 40 will beat 0-39 and 91-100, but lose to 41-90.
    elif (a - b) % size <= size / 2:
        return WIN
    else:
        return LOSE


def select_choice(problist):
    # Given an array of choice probabilities; for example, [45, 20, 35] meaning 45 to pick rock, 20 to pick
    # paper, and 35 to pick scissors, returns a choice at random.
    total = 0
    for item in problist:
        total += item
    choice = random.random()
    counter = 0
    listCounter = 0
    for item in problist:
        counter += item / total
        if counter > choice:
            return listCounter
        listCounter += 1
    return -1


def update_problist(algorithm, choice, multiplier=1.0):
    changes = [0, 0, 0]
    changes[choice] += multiplier * REWARDS[choice]
    # list2[choice] += multiplier * REWARDS[choice]
    # SPIRAL TIME HELL YEAH
    normalized_pt_a = normalize(algorithm)
    normalized_pt_b = normalize(add_array(algorithm, changes))
    point_a = convert_coords_to_triangle(normalized_pt_a[0], normalized_pt_a[1],
                                         normalized_pt_a[2])
    point_b = convert_coords_to_triangle(normalized_pt_b[0], normalized_pt_b[1], normalized_pt_b[2])
    # print("Point a is " + str(point_a) + "; Point b is " + str(point_b))
    change_vector = subtract_array(point_b, point_a)
    # print("Current changes (Cartesian) are " + str(change_vector))
    # print("Vector to angle is " + str(vector_to_angle(change_vector[0], change_vector[1])))
    resulting_vector = rotate(change_vector[0], change_vector[1], math.pi / 4)
    # print("Resulting vector is " + str(resulting_vector))
    resulting_point_b = add_array(resulting_vector, point_a)
    # print("Resulting point is " + str(resulting_point_b))

    changes = subtract_array(normalize(convert_triangle_to_coords(resulting_point_b[0], resulting_point_b[1]),
                                       3 * STARTING_VALUE), algorithm)
    return changes


if __name__ == "__main__":
    problist = []
    pickStats = []
    pickStatBase = []
    epochRewards = []
    epochProbabilities = []
    for i in range(SIZE):
        problist.append(STARTING_VALUE)
        pickStatBase.append(0)
        epochProbabilities.append([])
    overallStats = pickStatBase.copy()
    for i in range(EPOCHS):
        pickStats.append(pickStatBase.copy())
    for j in range(EPOCHS):
        gradient_problist = []
        for i in range(SIZE):
            gradient_problist.append(0)
        for i in range(ITERATIONS):
            combined_problist = []
            for k in range(SIZE):
                combined_problist.append(problist[k])
                if STATCOMBINE_BASE != 0:
                    factor = STATCOMBINE_EXP * 2 * j / EPOCHS - STATCOMBINE_EXP
                    combined_problist[k] += overallStats[k] * STATCOMBINE_BASE ** factor
            a = select_choice(combined_problist)
            b = select_choice(combined_problist)
            pickStats[j][a] += 1
            overallStats[a] += 1
            pickStats[j][b] += 1
            overallStats[b] += 1
            result = decide_game(a, b, SIZE)
            if result == WIN:
                problist = update_problist(problist, a)
                problist = update_problist(problist, b, DETERRENT * REWARDS[a] / REWARDS[b]\
                                           # * min(1.0, 2 * j / EPOCHS)\
                )
            elif result == LOSE:
                problist = update_problist(problist, b)
                problist = update_problist(problist, a, DETERRENT * REWARDS[b] / REWARDS[a])
            else:
                problist = update_problist(problist, a, TIE_REWARDS[a] * 2 / REWARDS[a])
        epochReward = []
        for i in range(SIZE):
            k = j - 1
            value = problist[i] - STARTING_VALUE
            while k >= 0:
                value -= epochRewards[k][i]
                k -= 1
            epochReward.append(value)
        epochRewards.append(epochReward)
        print("EPOCH " + str(j))
        print("USAGE STATS: " + str(pickStats[j]))
        print("REWARDS FOR EACH CHOICE: " + str(epochRewards[j]))
        total = 0
        probabilities = []
        for a in range(SIZE):
            total += problist[a]
        for a in range(SIZE):
            probabilities.append(problist[a] / total)
            epochProbabilities[a].append(probabilities[a])
        print("CURRENT STRATEGY: " + str(problist))
        print("CURRENT PROBABILITIES: " + str(probabilities))
    overall_stats = pickStatBase.copy()
    for i in range(EPOCHS):
        for j in range(SIZE):
            overall_stats[j] += pickStats[i][j]
    print("END")
    print("OVERALL USAGE STATS: " + str(overall_stats))
    for a in range(SIZE):
        print(  #"PROBABILITIES FOR CHOICE " + str(a) + ":" + \
              str(epochProbabilities[a]))
    for a in range(SIZE):
        for b in range(EPOCHS):
            print(pickStats[b][a], end=",")
        print("")

