import random
import math
import numpy as np
import matplotlib.pyplot as plt
import wave
import struct

STARTING_VALUE = 5
STARTING_RADIAN = -.447626 - math.pi
DETERRENT = -1
SIZE = 3
REWARDS = [1.5, 1, 1]
TIE_REWARDS = [0, 0, 0]
GRAPHED_CHOICE = 2
DERIVATIVE_ORDER = 0
FILENAME = "rps_startingvalue_2"
ITERATIONS = 1
EPOCHS = 1000
STARTING_STAT_EPOCH = 0 * 10 ** 5
ENDING_STAT_EPOCH = EPOCHS
MATCH_THRESHOLD = 2
AVERAGE = 2500
SPEED_FACTOR = 1

GRAPH_FACE_COLOR = []
GRAPH_INSIDE_COLOR = []
GRAPH_LINE_COLOR = []
BRIGHTNESS = random.randint(5, 40) / 5
print("Brightness: " + str(BRIGHTNESS))


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


def tweak_color(color, brightness):
    randomizer = random.randint(1, 5)
    if random.randint(1, 10) == 1:
        return 0
    else:
        return color ** (12 / (brightness ** .8 * randomizer))


def normalize(array, product=1):
    sum = 0
    return_array = []
    for item in array:
        sum += abs(item)
    for item in array:
        return_array.append(item * product / sum)
    return return_array


def zero_sum(array, sum=0):
    arraysum = 0
    return_array = []
    for item in array:
        arraysum += item
    for item in array:
        return_array.append(item + (sum - arraysum) / len(array))
    return return_array

def signal_to_wav(signal, fname, Fs):
    """Convert a numpy array into a wav file.

     Args
     ----
     signal : 1-D numpy array
         An array containing the audio signal.
     fname : str
         Name of the audio file where the signal will be saved.
     Fs: int
        Sampling rate of the signal.

    """
    data = struct.pack('<' + ('h'*len(signal)), *signal)
    wav_file = wave.open(fname, 'wb')
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(Fs)
    wav_file.writeframes(data)
    wav_file.close()


def integerize(item_list, avg_val):
    new_list = []
    for item in item_list:
        new_list.append(int((item - avg_val) * 100))
    return new_list


def derivative(statlist, dx=1):
    derivlist = [0]
    a = 1
    while a < len(statlist):
        derivlist.append((statlist[a] - statlist[a-1]) * dx)
        a += 1
    derivlist[0] = 4 * derivlist[1] - 2 * derivlist[2] - derivlist[3]
    return derivlist


def integral(statlist, dx=1, avg=0):
    intlist = [statlist[0] - avg]
    h = 1
    while h < len(statlist):
        intlist.append((intlist[-1] + statlist[h] - avg) * dx)
        h += 1
    return intlist


def d(statlist, index=1, avg=0, dx=1):
    while index > 0:
        statlist = derivative(statlist, dx)
        index -= 1
    while index < 0:
        statlist = integral(statlist, avg, dx)
        index += 1
    return statlist


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


if __name__ == "__main__":
    algorithm = []
    total = STARTING_VALUE * SIZE
    match = [GRAPHED_CHOICE, 500000]
    increasing = True
    stats = []
    peak_locations = []
    peaks = []
    es = []
    dy_values = [0]
    d2y_values = [0]
    area_values = []
    initial_changes = [5, 5, 5, 5, 5]
    angle_increment = 5
    peak_counter = 0
    e_storage = STARTING_VALUE
    for a in range(SIZE):
        algorithm.append(STARTING_VALUE)
        stats.append([])
    for a in range(EPOCHS):
        for b in range(ITERATIONS):
            changes = []
            for c in range(SIZE):
                change = 0
                for e in range(SIZE):
                    anti_zero_value = max(0, algorithm[c])
                    if anti_zero_value == 0:
                        pass
                        # print(1 / 0)
                    elif algorithm[c] < 0:
                        print("the value is below 0")
                        print(1/0)
                    if e == c:
                        change += TIE_REWARDS[c] * 2 * algorithm[e]
                    elif (c - e) % SIZE <= SIZE / 2:
                        change += algorithm[e] * REWARDS[c] * anti_zero_value * SPEED_FACTOR / total ** 2
                    else:
                        change -= algorithm[e] * REWARDS[e] * anti_zero_value * SPEED_FACTOR / total ** 2
                changes.append(change)
            if len(initial_changes) < 3:
                initial_changes.append(changes)
            elif angle_increment != 0:
                # print("Current changes are " + str(changes))
                change_sum = abs(changes[0]) + abs(changes[1]) + abs(changes[2])
                normalized_pt_a = normalize(algorithm)
                normalized_pt_b = normalize(add_array(algorithm, changes))
                pt_b = add_array(algorithm, changes)
                # print("Norm. pt a is " + str(normalized_pt_a))
                point_a = convert_coords_to_triangle(normalized_pt_a[0], normalized_pt_a[1],
                                                     normalized_pt_a[2])
                point_b = convert_coords_to_triangle(normalized_pt_b[0], normalized_pt_b[1], normalized_pt_b[2])
                # print("Point a is " + str(point_a) + "; Point b is " + str(point_b))
                change_vector = subtract_array(point_b, point_a)
                # print("Current changes (Cartesian) are " + str(change_vector))
                # print("Vector to angle is " + str(vector_to_angle(change_vector[0], change_vector[1])))
                resulting_vector = rotate(change_vector[0], change_vector[1], 0)
                # print("Resulting vector is " + str(resulting_vector))
                resulting_point_b = add_array(resulting_vector, point_a)
                # print("Resulting point is " + str(resulting_point_b))

                changes = subtract_array(normalize(convert_triangle_to_coords(resulting_point_b[0], resulting_point_b[1]),
                                                   3*STARTING_VALUE), algorithm)
                # changes = normalize(changes, change_sum)
                # changes = subtract_array(changes, algorithm)
                print("Updated changes are " + str(changes))
                # print("Updated changes (Cartesian) are " + str(convert_coords_to_triangle(changes[0], changes[1],
                                                                # changes[2])))
            else:
                # compute initial angle increment
                first_array = subtract_array(initial_changes[1], initial_changes[0])
                first_vector = convert_coords_to_triangle(first_array[0], first_array[1], first_array[2])
                first_angle = vector_to_angle(first_vector[0], first_vector[1])
                second_array = subtract_array(initial_changes[2], initial_changes[1])
                second_vector = convert_coords_to_triangle(second_array[0], second_array[1], second_array[2])
                second_angle = vector_to_angle(second_vector[0], second_vector[1])
                angle_increment = second_angle - first_angle
                print("Angle increment is " + str(angle_increment))
            if (changes[match[0]] > 0) is not increasing:
                # print("Changed direction at epoch " + str(a) + ", iteration "
                      # + str(b) + ", value " + str(algorithm[match[0]]))
                if increasing:
                    # peak_counter += 1
                    # if peak_counter == 50:
                    peak_locations.append(a * ITERATIONS + b)
                    peaks.append(algorithm[match[0]])
                    # peak_counter = 0
                increasing = not increasing
            if b == 0 and a > STARTING_STAT_EPOCH:
                dy_values.append(changes[match[0]])
                if len(area_values) > 0:
                    area_values.append(algorithm[match[0]] + area_values[-1] - AVERAGE)
                else:
                    area_values.append(algorithm[match[0]])
                if len(dy_values) > 1:
                    d2y_values.append(dy_values[-1] - dy_values[-2])
            if e_storage / math.e > algorithm[match[0]]:
                # print("e product found at location " + str(a * ITERATIONS + b) + ", value " + str(algorithm[match[0]]))
                e_storage /= math.e
                es.append(a * ITERATIONS + b)
            for c in range(SIZE):
                algorithm[c] += changes[c]
            if (algorithm[match[0]] - match[1]) ** 2 <= MATCH_THRESHOLD:
                print("Match at epoch " + str(a) + ", iteration " + str(b) + ", value " + str(algorithm[match[0]]))
        print("EPOCH " + str(a))
        print("CURRENT STRATEGY: " + str(algorithm))
        for b in range(SIZE):
            stats[b].append(algorithm[b])
    print("END")
    # for a in range(SIZE):
        # for b in stats[a]:
            # print(b, end=",")
        # print()
    # for a in peaks:
        # print(a, end=", ")
    # print()
    # for a in peak_locations:
        # print(a, end=",")
    # print()
    # for e in es:
        # print(e, end=",")
    x_coords = []
    for a in range(ENDING_STAT_EPOCH - STARTING_STAT_EPOCH):
        x_coords.append(STARTING_STAT_EPOCH + a * ITERATIONS)
    sin_coords = []
    # for a in x_coords:
        # sin_coords.append(8117.55 + 4349.2 * math.sin(x_coords[a] * 2 * math.pi / 556951 + STARTING_RADIAN))

    ENDING_RADIAN = -0.6536075264195716
    SUMMATION_STOP_POINT = 10 ** 5
    # x = ENDING_RADIAN * 556951 / 2 / math.pi
    x = 0
    x_values = []
    y_values = []
    triangle_x_values = []
    triangle_y_values = []
    dy_values = [0]
    d2y_values = [0]
    for a in range(EPOCHS):
        x_values.append(x + a * ITERATIONS)
    for x_value in x_values:
        y_value = 0
        k = 1
        k_power = 0
        while k_power < SUMMATION_STOP_POINT:
            k_power = k ** 3
            y_value += math.sin(k * x_value * 2 * math.pi / 556951) ** 2 / k_power
            k += 1
        y_values.insert(0, 3718.35 + 8698.4 * y_value)

    used_list = d(stats[match[0]], DERIVATIVE_ORDER)[STARTING_STAT_EPOCH:ENDING_STAT_EPOCH]
    for f in range(len(used_list)):
        s = STARTING_VALUE * 3
        triangle_x_values.append(convert_coords_to_triangle(stats[0][f]/s, stats[1][f]/s, stats[2][f]/s)[0])
        triangle_y_values.append(convert_coords_to_triangle(stats[0][f]/s, stats[1][f]/s, stats[2][f]/s)[1])
    average_value = 0
    for a in used_list:
        average_value += a
    average_value /= len(used_list)
    print("Average value: " + str(average_value))
    x_peaks = []
    for f in range(len(peaks)):
        x_peaks.append(f)
    for a in range(3):
        GRAPH_FACE_COLOR.append(tweak_color(random.random(), BRIGHTNESS))
        GRAPH_INSIDE_COLOR.append(tweak_color(random.random(), BRIGHTNESS))
        GRAPH_LINE_COLOR.append(tweak_color(random.random(), BRIGHTNESS))
    fig, ax = plt.subplots(facecolor=(GRAPH_FACE_COLOR[0], GRAPH_FACE_COLOR[1], GRAPH_FACE_COLOR[2]))
    ax.set_facecolor((GRAPH_INSIDE_COLOR[0], GRAPH_INSIDE_COLOR[1], GRAPH_INSIDE_COLOR[2]))
    # ax.plot(x_values, used_list, color=(GRAPH_LINE_COLOR[0], GRAPH_LINE_COLOR[1], GRAPH_LINE_COLOR[2]))
    ax.plot(triangle_x_values, triangle_y_values, color=(GRAPH_LINE_COLOR[0], GRAPH_LINE_COLOR[1], GRAPH_LINE_COLOR[2]))
    ax.plot([0, -.5, .5, 0], [math.sqrt(3)/2, 0, 0, math.sqrt(3)/2], color=(0, 0, 0))
    optimal_denominator = REWARDS[0] + 2
    starting_big = REWARDS[0]
    oa_x = convert_coords_to_triangle(1/optimal_denominator, starting_big/optimal_denominator, 1/optimal_denominator)[0]
    oa_y = convert_coords_to_triangle(1/optimal_denominator, starting_big/optimal_denominator, 1/optimal_denominator)[1]
    sn = .01
    ax.plot([oa_x - sn, oa_x - sn, oa_x + sn, oa_x + sn, oa_x - sn], [oa_y - sn, oa_y + sn, oa_y + sn, oa_y - sn,
                                                                      oa_y - sn], color=(1, 1, 1))
    # plt.yscale("log")
    # ax.plot(x_coords, stats[match[0]], 'xkcd:crimson')
    # ax.plot(x_peaks, peaks)
    # for a in range(SIZE):
        # ax.plot(x_coords, stats[a])
    # ax.plot(x_coords, y_values, 'C4')
    # signal_to_wav(numpy.array(integerize(used_list, average_value)), FILENAME, 441000)
    plt.show()