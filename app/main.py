#!/usr/bin/env python3
import json
import io

from flask import Flask, request, Response, abort

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from functions import lines_from_points, collinear_points, line_filter


# INPUT VARIABLES
points = set()  # populated by a user; no duplicate points can exist in the set
num = int()  # populated by a user; how many collinear points to consider
points_max_len = 100  # the limit of points in the set to preserve performance
lines = list()  # contains other lists of collinear points

app = Flask(__name__)


def to_json(data) -> str:
    return json.dumps(data)


def resp(code, data):
    return Response(status=code, mimetype="application/json", response=to_json(data))


@app.route('/point', methods=['POST', 'GET', 'DELETE'])
def new_point():
    if request.method == 'POST':
        try:
            px = int(request.form['x'])
            py = int(request.form['y'])
            if type(px) != int or type(py) != int:
                return abort(400, "Point coordinates must be integer values.")
            pt = (px, py)
            if len(points) < points_max_len:
                points.add(pt)
                return resp(200, {"Add new point": pt})
            else:
                return resp(304, f"The point was not added. You reached the maximum amount of points: {points_max_len}")
        except ValueError:
            return abort(400, "Point coordinates must be integer values.")
        except UnboundLocalError:
            return abort(400, "Point coordinates must be integer values.")
    elif request.method == 'GET':
        if len(points) == 0:
            return abort(404, "There are no points. Add some points first.")
        else:
            return resp(200, list(points))
    elif request.method == 'DELETE':
        points.clear()
        lines.clear()
        return resp(200, "All points and lines are deleted.")


@app.route('/lines/<int:n>', methods=['GET'])
def solution(n):
    global lines, num
    if type(n) != int or n < 3:
        return abort(400, "The number of requested collinear points must be an integer greater than or equal to 3.")
    elif len(points) == 0:
        return abort(404, "There are no points. Add some points first.")
    else:
        num = n
        segments = lines_from_points(points)
        lines = line_filter(collinear_points(points, segments), n)
        return resp(200, {f"Found {len(lines)} group(s) of collinear points": to_json(lines)})


@app.route('/plot.png')
def plot_png():
    if len(points) == 0:
        return abort(404, "There are no points to plot. Add some points first.")
    else:
        fig = create_figure()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png  ')


def create_figure():
    fig, ax = plt.subplots()
    plt.title(f"{len(points)} points, N = {num}")
    plt.grid()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().set_aspect("equal")
    pts_x, pts_y = [list(pt) for pt in zip(*points)]
    plt.scatter(pts_x, pts_y, c='black')
    for ln in lines:
        lns_pts_x, lns_pts_y = [list(pt) for pt in zip(*ln)]
        plt.plot(lns_pts_x, lns_pts_y)
    return fig


if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run()
