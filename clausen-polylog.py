import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import random
import cmath


def d(statlist, index=1, avg=0, dx=1):
    while index > 0:
        statlist = derivative(statlist, dx)
        index -= 1
    while index < 0:
        statlist = integral(statlist, avg, dx)
        index += 1
    return statlist


def derivative(statlist, dx=1):
    derivlist = [0]
    a = 1
    while a < len(statlist):
        derivlist.append((statlist[a] - statlist[a-1]) * dx)
        a += 1
    derivlist[0] = 2*derivlist[1]-derivlist[2]
    return derivlist


def integral(statlist, avg=0, dx=1):
    intlist = [statlist[0] - avg]
    a = 1
    while a < len(statlist):
        intlist.append((intlist[-1] + statlist[a] - avg) * dx)
        a += 1
    intlist[0] = 0
    return intlist


def tweak_color(color, brightness):
    randomizer = random.randint(1, 5)
    if random.randint(1, 10) == 1:
        return 0
    else:
        return color ** (12 / (brightness ** .8 * randomizer))


FUNCTION_ORDER = complex(2, 0)
STARTING_X = 0
ENDING_X = 10
VALUES = 10000
JUMP = (ENDING_X - STARTING_X) / VALUES
SECONDS = 1
SECONDS_PER_VALUE = SECONDS / VALUES
CALCULATIONS_PER_SECOND = 2 * 10 ** 6
CALCULATIONS = SECONDS_PER_VALUE * CALCULATIONS_PER_SECOND
SUMMATION_STOP_POINT = CALCULATIONS ** FUNCTION_ORDER.real

FIRST_INACCURACY = math.sin(CALCULATIONS * (STARTING_X + VALUES * JUMP / 2)) / SUMMATION_STOP_POINT
SECOND_INACCURACY = math.sin(CALCULATIONS * (STARTING_X + VALUES * JUMP / 2)) / (CALCULATIONS + 1) ** FUNCTION_ORDER
DIFFERENCE = (SECOND_INACCURACY / FIRST_INACCURACY).real

GRAPH_FACE_COLOR = []
GRAPH_INSIDE_COLOR = []
GRAPH_LINE_COLOR = []
BRIGHTNESS = random.randint(5, 40) / 5
print("Brightness: " + str(BRIGHTNESS))

for a in range(3):
    GRAPH_FACE_COLOR.append(tweak_color(random.random(), BRIGHTNESS))
    GRAPH_INSIDE_COLOR.append(tweak_color(random.random(), BRIGHTNESS))
    GRAPH_LINE_COLOR.append(tweak_color(random.random(), BRIGHTNESS))

print("Summation stop point is " + str(SUMMATION_STOP_POINT) + ". Inaccuracy will occur around " +
      str(math.sin(SECONDS_PER_VALUE * CALCULATIONS_PER_SECOND *
                   (STARTING_X + VALUES * JUMP / 2)) / SUMMATION_STOP_POINT), end=". ")
if DIFFERENCE > 1 or DIFFERENCE < 0:
    print("Inaccuracy estimate is unclear.")
else:
    print("Inaccuracy estimate is " + str(FIRST_INACCURACY / (1 - DIFFERENCE)))

x = STARTING_X
x_values = []
y_values = []
for a in range(VALUES):
    x_values.append(x + a * JUMP)
for x_value in x_values:
    polylogarithm_argument = math.e ** (complex(0, 1) * x_value)
    k = 1
    k_power = 0
    y_value = 0
    while k_power.real < SUMMATION_STOP_POINT:
        k_power = k ** FUNCTION_ORDER
        y_value += polylogarithm_argument ** k / k_power ** 1
        k += 1
    y_values.append(y_value.imag)
fig, ax = plt.subplots(facecolor=(GRAPH_FACE_COLOR[0], GRAPH_FACE_COLOR[1], GRAPH_FACE_COLOR[2]))
ax.set_facecolor((GRAPH_INSIDE_COLOR[0], GRAPH_INSIDE_COLOR[1], GRAPH_INSIDE_COLOR[2]))
ax.plot(x_values, d(y_values, 0), color=(GRAPH_LINE_COLOR[0], GRAPH_LINE_COLOR[1], GRAPH_LINE_COLOR[2]))
plt.show()