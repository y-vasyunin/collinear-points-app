import unittest
import random
import requests


endpoint = "http://127.0.0.1:5000/v1"

min_point = 4  # minimum number of points in one line to consider, including line ends
value_range = 110  # how many points to create in total


class TestAPI(unittest.TestCase):

    def test_a_clear_plot(self):
        r_pts = requests.delete(f"{endpoint}/points")
        self.assertEqual(r_pts.status_code, 200)

    def test_b_add_point(self):
        # generate random points
        val_r = int(value_range / 2)
        points = zip([random.randint(-val_r, val_r) for x in range(-val_r, val_r)],
                     [random.randint(-val_r, val_r) for y in range(-val_r, val_r)])
        for p in points:
            r_pt = requests.post(f"{endpoint}/points", data={"x": p[0], "y": p[1]})
            self.assertIn(r_pt.status_code, (201, 200))  # 201 — when a point is added;200 — when point limit is reached
        r_pt_er1 = requests.post(f"{endpoint}/points", data={"x": 3})
        self.assertEqual(r_pt_er1.status_code, 400)  # a point must have have integer coordinates
        r_pt_er2 = requests.post(f"{endpoint}/points", data={"x": 3, "y": 5.0})
        self.assertEqual(r_pt_er2.status_code, 400)  # a point must have have integer coordinates

    def test_c_get_points(self):
        r_pts = requests.get(f"{endpoint}/points")
        self.assertEqual(r_pts.status_code, 200)

    def test_d_get_lines(self):
        r_lns = requests.get(f"{endpoint}/lines/{min_point}")
        self.assertEqual(r_lns.status_code, 200)

    def test_e_get_plot(self):
        r_lns = requests.get(f"{endpoint}/plot")
        self.assertEqual(r_lns.status_code, 200)


if __name__ == "__main__":
    unittest.main()
