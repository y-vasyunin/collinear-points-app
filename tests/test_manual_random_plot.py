#!/usr/bin/env python3
import random
from main import collinear_points, lines_from_points, plot, line_filter
import time


start = time.time()

# INPUT VARIABLES
min_point = 4  # minimum number of points in one line to consider, including line ends
value_range = 250  # how far a random value can be from zero
points_x = [random.randint(-value_range, value_range) for x in range(-value_range, value_range)]
points_y = [random.randint(-value_range, value_range) for x in range(-value_range, value_range)]
points = set(zip(points_x, points_y))
lines = lines_from_points(points)

# COMPUTATION
selected_lines = line_filter(collinear_points(points, lines), min_point)
plot(points, selected_lines, min_point)

end = time.time()
print(end - start)
