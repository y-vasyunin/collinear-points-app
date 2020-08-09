#!/usr/bin/env python3
from itertools import combinations


def lines_from_points(pts: set) -> set:
    """Make all possible lines as a set of 2-dimension tuples, in sorted order, with no repeated elements."""

    return set(combinations(pts, 2))


def line_filter(lns: list, num: int) -> list:
    """Returns a list of lines that contain equal of greater amount of points than 'num'."""

    return list(filter(lambda ln: len(ln) >= num, lns))


def collinearity(xy: tuple, x1y1: tuple, x2y2: tuple) -> bool:
    """Check that a given point (x, y) is on a line ((x1, y1), (x2, y2)) using the equation of a straight line
    passing through two given points. Only points inside the line are considered, so if the given point is
    on one of the line ends, the function returns False."""

    x, y, x1, y1, x2, y2 = xy[0], xy[1], x1y1[0], x1y1[1], x2y2[0], x2y2[1]
    return (y1 - y2) * x + (x2 - x1) * y + (x1 * y2 - x2 * y1) == 0 and xy not in {x1y1, x2y2}


def collinear_points(pts: set, lns: set) -> list:
    selected_lines = list()
    for seg in lns:
        col_points = set(seg)
        for p in pts:
            if collinearity(p, seg[0], seg[1]):
                col_points.add(p)
        if len(col_points) > 2:  # consider only lines with 3 or more points
            selected_lines.append(col_points)
    selected_lines = set(frozenset(ln) for ln in selected_lines)  # remove duplicate lines with a different point order
    solution_lines = list()
    for i in selected_lines:
        solution_lines.append(list(i))
    return solution_lines
