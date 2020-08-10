#!/usr/bin/env python3
from itertools import combinations


def lines_from_points(pts: set) -> set:
    """Make all possible lines as a set of 2-dimension tuples, in sorted order, with no repeated elements."""

    s = [list(p) for p in combinations(pts, 2)]
    ss = set()
    for i in range(len(s)):  # remove lines with neighboring points
        if not abs(s[i][0][0] - s[i][1][0]) <= 1 and not abs(s[i][0][1] - s[i][1][1]) <= 1:
            ss.add(tuple(s[i]))
    return ss


def line_filter(lns: list, num: int) -> list:
    """Returns a list of lines that contain equal of greater amount of points than 'num'."""

    return list(filter(lambda ln: len(ln) >= num, lns))


def collinearity(xy: tuple, x1y1: tuple, x2y2: tuple) -> bool:
    """Checks that a given point (x, y) is on a line ((x1, y1), (x2, y2)) using the equation of a straight line
    passing through two given points. Only points inside the line are considered, so if the given point is
    on one of the line ends, the function returns False."""

    x, y, x1, y1, x2, y2 = xy[0], xy[1], x1y1[0], x1y1[1], x2y2[0], x2y2[1]
    return (y1 - y2) * x + (x2 - x1) * y + (x1 * y2 - x2 * y1) == 0 and xy not in {x1y1, x2y2}


def collinear_points(pts: set, lns: set) -> list:
    """Takes two sets, points and lines, and returns a list of all collinear points discovered in the input data."""

    selected_lines = list()
    for seg in lns:  # TODO: this loop is the most time-consuming thing; try to optimize it
        col_points = set(seg)  # for every line, store available collinear points in this temporary set
        for p in pts:
            if collinearity(p, seg[0], seg[1]):
                col_points.add(p)
        if len(col_points) > 2:  # consider only lines with more than two points
            selected_lines.append(col_points)
    selected_lines = set(frozenset(ln) for ln in selected_lines)  # remove duplicate lines with a different point order
    solution_lines = list()
    for i in selected_lines:
        solution_lines.append(list(i))
    return solution_lines
