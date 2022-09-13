import math
import matplotlib.pyplot as plt

EPOCHS = 1000
ITERATIONS = 1
DX = 0.1
STARTING_X = 0

y_values = []
x_values = []
for a in range(EPOCHS):
    x_values.append(a * ITERATIONS)
current_value = 0
for a in range(EPOCHS):
    for b in range(ITERATIONS):
        current_value += math.cos(STARTING_X + (100 * a + b) * DX)
    y_values.append(current_value)
fig, ax = plt.subplots()
ax.plot(x_values, y_values)
plt.show()