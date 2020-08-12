import io

from flask import Flask, request, Response, jsonify, redirect

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg

from main import CartesianPlane

space = CartesianPlane(100)  # empty 2D space
num = int()
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
            if len(space.points) < space.point_limit:
                space.add_point(px, py)
                return f"Add a new pont: {(px, py)}", 201
            else:
                return f"A point wasn't added. You already reached {space.point_limit} points.", 200
        except Exception:
            return "Point must have two integer coordinates: x=int&y=int.", 400

    if request.method == "GET":
        if len(space.points) == 0:
            return "There are no points. Add some points first: [POST]/points.", 200
        else:
            return jsonify(points=list(space.points)), 200
    elif request.method == "DELETE":
        if len(space.points) > 0:
            old_pts = len(space.points)
            space.clear()
            return f"All {old_pts} point(s) were deleted.", 200
        else:
            return f"There are no points to delete.", 200


@app.route(f"/v{api_version}/lines/<int:n>", methods=["GET"])
def solution(n):
    global num
    if type(n) != int or n < 3:
        return "The number of requested collinear points must be an integer greater than or equal to 3.", 200
    elif len(space.points) == 0:
        return "There are no points. Add some points first: [POST]/points.", 200
    else:
        num = n
        space.find_collinear_points(num)
        return jsonify(collinear_points=space.lines,
                       message=f"Found {len(space.lines)} group(s) of collinear points"
                               f"within {len(space.points)} points."), 200


@app.route(f"/v{api_version}/plot")
def plot_png():
    if len(space.points) == 0:
        return "There are no points to plot. Add some points first: [POST]/points.", 200
    else:
        fig = create_figure()
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png'), 200


def create_figure():
    fig, ax = plt.subplots()
    plt.title(f"{len(space.points)} points, {len(space.lines)} lines found with N = {num}")
    plt.grid()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().set_aspect("equal")
    pts_x, pts_y = [list(pt) for pt in zip(*space.points)]
    plt.scatter(pts_x, pts_y, c='black')
    for ln in space.lines:
        lns_pts_x, lns_pts_y = [list(pt) for pt in zip(*ln)]
        plt.plot(lns_pts_x, lns_pts_y)
    return fig


if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run()
