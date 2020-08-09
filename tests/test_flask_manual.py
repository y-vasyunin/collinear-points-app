#!/usr/bin/env python3
import random
import requests

endpoint = "http://127.0.0.1:5000"

# INPUT DATA
min_point = 4  # minimum number of points in one line to consider, including line ends
value_range = 100  # how many points to create
value_range = int(value_range/2)
points_x = [random.randint(-value_range, value_range) for x in range(-value_range, value_range)]
points_y = [random.randint(-value_range, value_range) for y in range(-value_range, value_range)]
points = zip(points_x, points_y)

# Delete points
rdel = requests.delete(f"{endpoint}/point")
print(f"Delete all points: code {rdel.status_code}, {rdel.reason}")

# Add points
for p in points:
    rp = requests.post(f"{endpoint}/point", data={'x': p[0], 'y': p[1]})
    print(f"{p}: {rp.status_code}, {rp.reason}")

# Get lines
rl = requests.get(f"{endpoint}/lines/{min_point}")
print(rl.content)
