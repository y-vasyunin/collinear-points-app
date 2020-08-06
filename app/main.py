#!/usr/bin/env python3

import itertools
import matplotlib.pyplot as plt
from functools import wraps
from flask import Flask, request, Response, redirect


def collinearity(x, y, line):
    """This function checks that a given point (x, y) is on a line
    using the equation of a straight line passing through two given points

    Parameters:
        x (int): coordinate of the input point
        y (int): coordinate of the input point
        line (tuple): a line against which the point collinearity is checked - must be a tuple with two sets
            of integer coordinates like ((x1, y1), (x2, y2))
    Returns:
        bool: True or False"""

    if not len(line) == 2 or not list(map(type, line)) == [tuple, tuple]:
        raise TypeError("A line has to be a 2-dimension tuple with int-coordinates, like ((1, 2), (5, 6)).")
    # make a flat list from a two-dimensional line tuple
    x1, y1, x2, y2 = [coord for point in line for coord in point]
    # don't consider points on the line ends
    if (y1 - y2) * x + (x2 - x1) * y + (x1 * y2 - x2 * y1) == 0 and (x, y) not in line:
        return True
    else:
        return False


def clean_plot():
    return psycopg2.connect(host="dev.geospatial.team", dbname="projects", user="rest_app",
                            password="uKGUeV3WrK7fCl7Qw8bj")


# DEFAULT VARIABLES

point_num = 3  # minimum number of points in one line to consider, including line ends
points_x = [1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 8, 9, 10, 10, 10, 10, 10]  # x coordinates of sample points
points_y = [4, 7, 1, 3, 9, 5, 10, 1, 9, 3, 6, 5, 10, 9, 8, 4, 2]  # y coordinates of sample points
points = set(zip(points_x, points_y))
lines = set(itertools.combinations(points, 2))  # make lines as 2-dimension tuples in sorted order, no repeated elements

# COLLINEARITY CHECKING

selected_lines = list()
for segment in lines:
    collinear_points = set(segment)
    for p in points:
        if collinearity(p[0], p[1], segment):
            collinear_points.add(p)
    if len(collinear_points) >= point_num:
        selected_lines.append(collinear_points)
selected_lines = list(set(frozenset(i) for i in selected_lines))  # remove duplicate lines with a different point order

# VISUALIZATION

fig, ax = plt.subplots()
major_ticks = list(range(1, 11))
ax.set_xticks(major_ticks)
ax.set_yticks(major_ticks)
plt.grid()
plt.gca().set_aspect("equal")
plt.title(f"N = {point_num}")
for i in selected_lines:
    line_x = list((x[0] for x in i))
    line_y = list((y[1] for y in i))
    plt.plot(line_x, line_y)
plt.scatter(points_x, points_y, c='black')
plt.show()
