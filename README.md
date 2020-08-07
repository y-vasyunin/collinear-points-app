# COLLINEAR POINTS APP

## What is this repository for?
Python code in this repo serves for solving a specific problem within a developer candidate test. Licensed under the GPLv3.

## Repo structure ##

## Problem description

Given a set of feature points in the bidimensional plane, determine every line that contains at least N or more collinear points (point coordinate in integer values).

![Diagrams](resources/diagram.png)

Manage data through this REST API:

* `[POST]/point` adds a new point in space
* `[GET]/lines/{n}` gets all lines passing through at least N points (a line segment is a set of collinear points)

## Solution
1. Create all possible pairs of points in the 2d space, so that each pair `(x1, y1)` and `(x2, y2)` defines a strait line. 

2. For every line, check that a given point `(x, y)`, if it is not already on the line ends, is on that straight line using the following equation:
    ```
    (y1 - y2) * x + (x2 - x1) * y + (x1 * y2 - x2 * y1) == 0
   ```
3. If the given point `(x, y)` is collinear with the line, add point coordinates to a set of line coordinates.
4. Repeat for all remaining points.

This algorithm is realized in a web application. The point coordinates are stored data for the lifetime of an application, how should that be done?

## How do I get set up?

### Python Dependencies

##№ Deployment instructions

## Performance

* Amount of N (collinear points in a segment) doesn't affect the runtime.
* The bottleneck is the collinearity check, which runs as a nested loop (for every line segment check every point) and increases computing time exponentially, as shown on a graph below. It has to be redesigned.

    ![Diagrams](resources/execution_test1.png)

    ![Diagrams](resources/execution_test2.png)

* A possible approach is to somehow filter out irrelevant points before putting them inside the loop:

## Who do I talk to?

* Repo owner: [Yaroslav Vasyunin](https://www.linkedin.com/in/vasyunin/)