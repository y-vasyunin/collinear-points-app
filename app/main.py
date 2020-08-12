#!/usr/bin/env python3
from itertools import combinations
import warnings


def collinearity(xy: tuple, x1y1: tuple, x2y2: tuple) -> bool:
    """Checks that a given point (x, y) is on a line ((x1, y1), (x2, y2)) using the equation of a straight line
    passing through two given points. Only points inside the line are considered, so if the given point is
    on one of the line ends, the function returns False."""

    x, y, x1, y1, x2, y2 = xy[0], xy[1], x1y1[0], x1y1[1], x2y2[0], x2y2[1]
    return (y1 - y2) * x + (x2 - x1) * y + (x1 * y2 - x2 * y1) == 0 and xy not in {x1y1, x2y2}


def line_filter(lns: list, num: int) -> list:
    """Returns a list of lines that contain equal of greater amount of points than 'num'."""

    return list(filter(lambda ln: len(ln) >= num, lns))


class CartesianPlane:
    """An 2D space object that can contain points and lines, and have methods to identify collinear points."""

    points = set()
    lines = list()

    def __init__(self, point_limit: int = 100):
        self.point_limit = point_limit
        if type(point_limit) != int:
            raise TypeError("Point limit must be an integer.")

    def add_point(self, x: int, y: int):
        """Create a new 2D point."""

        if type(x) != int or type(y) != int:
            raise TypeError("Point coordinates must be integer values.")
        else:
            if len(self.points) < self.point_limit:
                coords = (x, y)
                self.points.add(coords)
            else:
                warnings.warn(f"You reached the maximum limit of points in the space, which is {self.point_limit}.")

    def find_collinear_points(self, num: int):
        """Get lines composed from at least <num> collinear points. <num> can't be less than 3."""

        if type(num) != int:
            raise TypeError("Minimum number of collinear points in a line must be an integer.")
        elif num < 3:
            raise ValueError("Minimum number of collinear points in a line can't be less than 3.")
        elif len(self.points) < 3:
            warnings.warn(f"Add at least 3 points before finding collinear groups. Now you have {len(self.points)}.")
        else:
            s = [list(p) for p in combinations(self.points, 2)]
            ss = set()  # all line combinations without duplicates
            for i in range(len(s)):  # remove lines with neighboring points
                if not abs(s[i][0][0] - s[i][1][0]) <= 1 and not abs(s[i][0][1] - s[i][1][1]) <= 1:
                    ss.add(tuple(s[i]))
            selected_lines = list()
            for seg in ss:  # TODO: this loop is the most time-consuming thing; try to optimize it
                col_points = set(seg)  # for every line, store available collinear points in this temporary set
                for p in self.points:
                    if collinearity(p, seg[0], seg[1]):
                        col_points.add(p)
                if len(col_points) > 2:  # consider only lines with more than two points
                    selected_lines.append(col_points)
            selected_lines = set(
                frozenset(ln) for ln in line_filter(selected_lines, num))  # remove duplicate lines with a different point order
            for i in selected_lines:
                self.lines.append(list(i))
            return f"Found {len(self.lines)} group(s) of collinear points"

    def clear(self):
        self.points.clear()
        self.lines.clear()
