#!/usr/bin/env python3
import io

from flask import Flask, request, Response, jsonify, redirect

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg

from functions import lines_from_points, collinear_points, line_filter


points = set()  # populated by a user; no duplicate points can exist in the set
num = int()  # populated by a user; how many collinear points to consider
points_max_len = 100  # the limit of points in the set to preserve performance
lines = list()  # contains a list of collinear points
api_version = 1

app = Flask(__name__)


@app.route("/")
def root():
    return redirect(f"/v{api_version}")


@app.route(f"/v{api_version}", methods=["GET"])
def summary():
    return f"Collinear Points App, version {api_version}. Documentation available at "\
           f"https://github.com/y-vasyunin/collinear-points-app. "\
           "This API is used to determine every line that contains at least N or more collinear points in the "\
           "bi-dimensional plane. Refer to the documentation to see available resource URIs.", 200


@app.route(f"/v{api_version}/points", methods=["POST", "GET", "DELETE"])
def new_point():
    if request.method == "POST":
        try:
            px = int(request.form["x"])
            py = int(request.form["y"])
            if type(px) != int or type(py) != int:
                return "Point coordinates must be integer values: x=int&y=int.", 400
            pt = (px, py)
            if len(points) < points_max_len:
                points.add(pt)
                return f"Add a new pont: {pt}", 201
            else:
                return f"A point wasn't added. You already reached {points_max_len} points.", 200
        except Exception:
            return "Point coordinates must be integer values: x=int&y=int.", 422

    if request.method == "GET":
        if len(points) == 0:
            return "There are no points. Add some points first: [POST]/points.", 200
        else:
            return jsonify(points=list(points)), 200
    elif request.method == "DELETE":
        if len(points) > 0:
            old_pts = len(points)
            points.clear()
            lines.clear()
            return f"All {old_pts} point(s) were deleted.", 200
        else:
            return f"There are no points to delete.", 200


@app.route(f"/v{api_version}/lines/<int:n>", methods=["GET"])
def solution(n):
    global lines, num
    if type(n) != int or n < 3:
        return "The number of requested collinear points must be an integer greater than or equal to 3.", 200
    elif len(points) == 0:
        return "There are no points. Add some points first: [POST]/points.", 200
    else:
        num = n
        segments = lines_from_points(points)
        lines = line_filter(collinear_points(points, segments), n)
        return jsonify(collinear_points=lines,
                       message=f"Found {len(lines)} group(s) of collinear points within {len(points)} points."), 200


@app.route(f"/v{api_version}/plot")
def plot_png():
    if len(points) == 0:
        return "There are no points to plot. Add some points first: [POST]/points.", 200
    else:
        fig = create_figure()
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png'), 200


def create_figure():
    fig, ax = plt.subplots()
    plt.title(f"{len(points)} points, {len(lines)} lines found with N = {num}")
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
