#!/usr/bin/env python3
import time
import random
import requests

start = time.time()

endpoint = "http://127.0.0.1:5000"
# endpoint = "https://collinearity-checker.herokuapp.com"

# Input data
min_point = 4  # minimum number of points in one line to consider, including line ends
value_range = 110  # how many points to create
value_range = int(value_range/2)
points_x = [random.randint(-value_range, value_range) for x in range(-value_range, value_range)]
points_y = [random.randint(-value_range, value_range) for y in range(-value_range, value_range)]
points = zip(points_x, points_y)

# Delete points
rdel = requests.delete(f"{endpoint}/point")
print(rdel.json()["message"])

# Add points
for p in points:
    rp = requests.post(f"{endpoint}/point", data={'x': p[0], 'y': p[1]})
    print(f"{p}: Code {rp.status_code}, {rp.reason}")

# Get lines
rl = requests.get(f"{endpoint}/lines/{min_point}")
print(f'\n{rl.json()["message"]}')
# print(rl.content)

end = time.time() - start
print(f"\nScript finished in {round(end, 3)} s.")
