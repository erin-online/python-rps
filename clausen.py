import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import random
import cmath


def derivative(statlist, dx=1):
    derivlist = [0]
    a = 1
    while a < len(statlist):
        derivlist.append((statlist[a] - statlist[a-1]) * dx)
        a += 1
    derivlist[0] = 2*derivlist[1]-derivlist[2]
    return derivlist


def integral(statlist, dx=1, avg=0):
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


FUNCTION_ORDER = 2
STARTING_X = 0
ENDING_X = 5
VALUES = 1000
JUMP = (ENDING_X - STARTING_X) / VALUES
SECONDS = .1
SECONDS_PER_VALUE = SECONDS / VALUES
CALCULATIONS_PER_SECOND = 2 * 10 ** 6
CALCULATIONS = SECONDS_PER_VALUE * CALCULATIONS_PER_SECOND
SUMMATION_STOP_POINT = CALCULATIONS ** FUNCTION_ORDER

FIRST_INACCURACY = math.sin(CALCULATIONS * (STARTING_X + VALUES * JUMP / 2)) / SUMMATION_STOP_POINT
SECOND_INACCURACY = math.sin(CALCULATIONS * (STARTING_X + VALUES * JUMP / 2)) / (CALCULATIONS + 1) ** FUNCTION_ORDER
DIFFERENCE = (SECOND_INACCURACY / FIRST_INACCURACY)

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
dy_values = [0]
d2y_values = [0]
for a in range(VALUES):
    x_values.append(x + a * JUMP)
for x_value in x_values:
    y_value = 0
    k = 1
    k_power = 0
    latter_x = ENDING_X - x_value
    while k_power < SUMMATION_STOP_POINT:
        k_power = k ** FUNCTION_ORDER
        y_value += (math.sin(k * x_value) / k_power)
        k += 1
    if len(y_values) > 0:
        dy_values.append((y_value - y_values[-1]) / JUMP)
    if len(dy_values) > 1:
        d2y_values.append((dy_values[-1] - dy_values[-2]))
    y_values.append(y_value)
fig, ax = plt.subplots(facecolor=(GRAPH_FACE_COLOR[0], GRAPH_FACE_COLOR[1], GRAPH_FACE_COLOR[2]))
ax.set_facecolor((GRAPH_INSIDE_COLOR[0], GRAPH_INSIDE_COLOR[1], GRAPH_INSIDE_COLOR[2]))
ax.plot(x_values, y_values, color=(GRAPH_LINE_COLOR[0], GRAPH_LINE_COLOR[1], GRAPH_LINE_COLOR[2]))
plt.show()
