#!/usr/bin/env python3
import io

from flask import Flask, request, Response, abort, jsonify

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from functions import lines_from_points, collinear_points, line_filter


points = set()  # populated by a user; no duplicate points can exist in the set
num = int()  # populated by a user; how many collinear points to consider
points_max_len = 100  # the limit of points in the set to preserve performance
lines = list()  # contains a list of collinear points

app = Flask(__name__)


@app.route('/', methods=['GET'])
def summary():
    return jsonify(
        name="Collinear Points App", version=0.1, documentation="https://github.com/y-vasyunin/collinear-points-app",
        description="This API is used to determine every line that contains at least N or more collinear points in the "
                    "bi-dimensional plane. Refer to the documentation to see available resource URIs."), 200


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
                return jsonify(message=f"Added a new point: {pt}"), 200
            else:
                return jsonify(message=f"A point wasn't added. You already reached {points_max_len} points."), 304
        except (ValueError, UnboundLocalError):
            return abort(400, "Point coordinates must be integer values.")
    elif request.method == 'GET':
        if len(points) == 0:
            return abort(404, "There are no points. Add some points first: [POST]/point.")
        else:
            return jsonify(points=list(points)), 200
    elif request.method == 'DELETE':
        old_pts = len(points)
        points.clear()
        lines.clear()
        return jsonify(message=f"{old_pts} points have been deleted. You have 0 points now."), 200


@app.route('/lines/<int:n>', methods=['GET'])
def solution(n):
    global lines, num
    if type(n) != int or n < 3:
        return abort(400, "The number of requested collinear points must be an integer greater than or equal to 3.")
    elif len(points) == 0:
        return abort(404, "There are no points. Add some points first: [POST]/point.")
    else:
        num = n
        segments = lines_from_points(points)
        lines = line_filter(collinear_points(points, segments), n)
        return jsonify(collinear_points=lines,
                       message=f"Found {len(lines)} group(s) of collinear points within {len(points)} points."), 200


@app.route('/plot.png')
def plot_png():
    if len(points) == 0:
        return abort(404, "There are no points to plot. Add some points first: [POST]/point.")
    else:
        fig = create_figure()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig, ax = plt.subplots()
    plt.title(f"{len(points)} points, N = {num}, Found {len(lines)} lines")
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
