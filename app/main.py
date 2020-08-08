#!/usr/bin/env python3
import itertools
import matplotlib.pyplot as plt


def lines_from_points(pts) -> set:
    """Make all possible lines as a set of 2-dimension tuples, in sorted order, with no repeated elements."""
    return set(itertools.combinations(pts, 2))


def point_validation(coords) -> bool:
    """Conforms a single point to fit the specified format (x, y)."""
    return type(coords) == tuple and list(map(type, coords)) == [int, int] and len(coords) == 2


def line_filter(lns, num) -> list:
    """Returns a list of lines that contain equal of greater amount of points than 'num'."""
    return list(filter(lambda ln: len(ln) >= num, lns))


def collinearity(xy, x1y1, x2y2):
    """This function checks that a given point (x, y) is on a line ((x1, y1), (x2, y2))
    using the equation of a straight line passing through two given points.
    Only points inside the line are considered, so
    if the given point is on one of the line ends, the function returns False.

    Parameters:
        xy (tuple): coordinates of the input point (int, int)
        x1y1 (tuple): coordinates of the first line point (int, int)
        x2y2 (tuple): coordinates of the second line point (int, int)
    Returns:
        bool:"""

    x, y, x1, y1, x2, y2 = xy[0], xy[1], x1y1[0], x1y1[1], x2y2[0], x2y2[1]
    return (y1 - y2) * x + (x2 - x1) * y + (x1 * y2 - x2 * y1) == 0 and xy not in {x1y1, x2y2}


def plot(pts, lns, num):
    """Put all points and lines on a plot

    Parameters:
        pts (set): a set of tuples with the length of 2 containing coordinates of all point (int, int)
        lns (set): a set of unlimited-length tuples containing collinear points
        num (int): the minimum number of collinear points to consider
    Returns:
        bool:"""
    pts_len = len(pts)
    plt.title(f"{pts_len} points, N = {num}")
    plt.grid()
    plt.gca().set_aspect("equal")
    pts_x, pts_y = [list(pt) for pt in zip(*pts)]
    plt.scatter(pts_x, pts_y, c='black')
    for ln in lns:
        lns_pts_x, lns_pts_y = [list(pt) for pt in zip(*ln)]
        plt.plot(lns_pts_x, lns_pts_y)
    return plt.show()


def collinear_points(pts, lns) -> set:
    selected_lines = list()
    for seg in lns:
        col_points = set(seg)
        for p in pts:
            if collinearity(p, seg[0], seg[1]):
                col_points.add(p)
        if len(col_points) > 2:  # consider only lines with 3 or more points
            selected_lines.append(col_points)
    selected_lines = set(frozenset(ln) for ln in selected_lines)  # remove duplicate lines with a different point order
    return selected_lines
