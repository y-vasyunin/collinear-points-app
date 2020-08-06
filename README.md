# Collinear Points App

All code in this repo serves for a developer candidate test.

## Problem Statement

Given a set of feature points in the bidimensional plane, determine every line that contains at least N or more collinear points (point coordinate in integer values).

Manage data through this REST API:

* `[POST]/point` adds a new point in space
* `[GET]/lines/{n}` gets all lines passing through at least N points (a line segment is a set of collinear points)
