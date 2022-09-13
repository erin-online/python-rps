# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
ITERS = 1000

ROCK = 0
PAPER = 1
SCISSORS = 2

P1_WIN = [10, 1, 2]
DRAW = [0, 0, 0]
P2_WIN = [-10, -1, -2]

def run_game(p1, p2):
    # Use a breakpoint in the code line below to debug your script.
    if p1 == p2:  # Press Ctrl+F8 to toggle the breakpoint.
        return DRAW[p1]
    elif p2 == get_losing_option(p1):
        return P1_WIN[p1]
    else:
        return P2_WIN[p2]


def update_primes(primes, resultA, resultB, resultC):
    return [primes[0] + resultA, primes[1] + resultB, primes[2] + resultC]


def update_ai(primes, ai):
    primes_sum = primes[0] ** 3 + primes[1] ** 3 + primes[2] ** 3
    if primes_sum > 0:
        return normalize([ai[0] + primes[0] / primes_sum, ai[1] + primes[1] / primes_sum, ai[2] + primes[2] / primes_sum])
    else:
        return [1/3, 1/3, 1/3]


def update_ai_small(ai, choices):
    for a in range(3):
        ai[a] += choices[a] / 100
    return ai


def select_option(distribution):
    choice = random.random()
    if choice < distribution[0]:
        return ROCK
    elif choice < distribution[0] + distribution[1]:
        return PAPER
    else:
        return SCISSORS

def get_losing_option(winner):
    if winner > 0:
        return winner - 1
    else:
        return 2


def get_winning_option(loser):
    if loser < 2:
        return loser + 1
    else:
        return 0


def normalize(list):
    for i in range(len(list)):
        if list[i] < 0:
            list[i] = 0
    sum = list[0] + list[1] + list[2]
    for i in range(len(list)):
        list[i] /= sum
    return list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    primes = [0, 0, 0]
    results = [0, 0, 0]
    later_half_results = [0, 0, 0]
    ai = [1/3, 1/3, 1/3]
    for i in range(ITERS):
        if i == ITERS / 2:
            print("Decision-making at halfway point: " + str(ai))
        p1_option = select_option(ai)
        p2_option = select_option(ai)
        result = run_game(p1_option, p2_option)
        choices_feedback = [0, 0, 0]
        if result < 0:
            choices_feedback[p2_option] -= result
            choices_feedback[get_losing_option(p2_option)] += result
            results = update_primes(results, choices_feedback[0], choices_feedback[1], choices_feedback[2])
            if i > ITERS / 2:
                later_half_results = update_primes(later_half_results, choices_feedback[0], choices_feedback[1], choices_feedback[2])
            choices_feedback[get_winning_option(p2_option)] += P1_WIN[get_winning_option(p2_option)] / 5
        else:
            choices_feedback[p1_option] += result
            choices_feedback[get_losing_option(p1_option)] -= result
            results = update_primes(results, choices_feedback[0], choices_feedback[1], choices_feedback[2])
            if i > ITERS / 2:
                later_half_results = update_primes(later_half_results, choices_feedback[0], choices_feedback[1], choices_feedback[2])
            choices_feedback[get_winning_option(p1_option)] += P1_WIN[get_winning_option(p1_option)] / 5

        primes = update_primes(primes, choices_feedback[0], choices_feedback[1], choices_feedback[2])
        ai = update_ai_small(ai, choices_feedback)
        ai = update_ai(primes, ai)
    print("Results: " + str(results))
    print("Results from second half: " + str(later_half_results))
    print("Primes: " + str(primes))
    print("Decision-making: " + str(ai))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
