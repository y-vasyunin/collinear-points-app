# COLLINEAR POINTS APP

## What is his repository for?
Python code in this repo serves for solving a specific problem within a developer candidate test. It is a Flask-based web application that provides a simple API to solve the following problem, licensed under the GPLv3.

## Problem description

Given a set of feature points in the bidimensional plane, determine every line that contains at least N or more collinear points (point coordinate in integer values).

![Diagrams](resources/testing_plot.png)

Manage data through this REST API:

* `[POST]/point` adds a new point in space
* `[GET]/lines/{n}` gets all lines passing through at least N points (a line segment is a set of collinear points)

## Repo structure ##

- `app/main.py` — the main application script.
- `app/fucntions.py` — functions used by the main script.
- `app/Procfile` — lists the process types in an application. Each process type is a declaration of a command that is executed when a container of that process type is started. Used for hosing on [Heroku](https://www.heroku.com).
- `app/requirements.txt` — necessary Python libraries
- `app/runtime.txt` — specifies a Python runtime for [Heroku](https://www.heroku.com).
- `resources/*` — pictures for this README.
- `tests/test_algorithm_auto.py` — a unit test that can be run automatically to assert the correctness of the collinearity check. It uses hardcoded validation data, which are shown on a plot in the beginning of this README.
- `tests/test_flask_manual.py` — a manual test for a running Flask application to experiment with API.

## Problem solution

1. Create all possible pairs of points in the 2d space, so that each pair `(x1, y1)` and `(x2, y2)` defines a strait line. 

2. For every line, check that a given point `(x, y)`, if it is not already on the line ends, is on that straight line using the following equation:
    ```
    (y1 - y2) * x + (x2 - x1) * y + (x1 * y2 - x2 * y1) == 0
   ```
3. If the given point `(x, y)` is collinear with the line, add point coordinates to a set of line coordinates.
4. Repeat for all remaining points.

This algorithm is realized in a web application. The point coordinates are stored data for the lifetime of an application.

## How do I get set up?

Make sure that the `app` folder is a working directory for the app, otherwise import statements may not work. Run `main.py`. It will start a Flask web app on your localhost, port 5000. By default, 2d space doesn't have any points in it.

Use the following requests to interact with the API (examples are given for a command line with the `curl` utility installed).

Add one point (x: -10, y: 15)
```
curl -X POST -F "x=-10" -F "y=15" http://127.0.0.1/point
```
To see all the points you added:
```
curl -X GET http://127.0.0.1:5000/point
```
Please note that if you try to add more than 100 points, you get a response code `304`. To clean all you point, do this:
```
curl -X DELETE http://127.0.0.1:5000/point
```
After you filled the space with points, you can estimate, which of them are collinear, by providing a minimum number of points at the end of the url. The following request will return only line segments with 5 or more points:
```
curl -X GET http://127.0.0.1:5000/line/5
```
Finally, as you detected the collinear points and line segments, you can plot them (every time you run `[GET]/line/{n}`, you reset the plot):
```
curl -X GET http://127.0.0.1:5000/plot.png
```

## Performance

* Amount of the requested N (collinear points in a segment) doesn't affect the performance.
* The bottleneck of the app is the collinearity check, which runs as a nested loop, i.e. for every line segment it checks every point. This approach increases computing time exponentially, as shown on a graph below. That is why the maximum amount of points to plot is limited to 100.

    ![Diagrams](resources/execution_test1.png)

    ![Diagrams](resources/execution_test2.png)

A good approach to boost the app speed would be to use spatial indices for a preliminary filtering of irrelevant points for every segment (before going to the nested loop). It should be possible to implement this solution using [Shapely](https://pypi.org/project/Shapely/).

## Who do I talk to?

* Repo owner: [Yaroslav Vasyunin](https://www.linkedin.com/in/vasyunin/)