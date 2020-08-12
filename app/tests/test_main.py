import unittest

from main import CartesianPlane
from tests.validation_data import VALIDATION_POINTS, VALIDATION_LINES

space = CartesianPlane(150)
pts = space.points
lns = space.lines


class TestPoints(unittest.TestCase):

    def test_points(self):
        len1 = len(pts)
        space.add_point(1, 1)
        len2 = len(pts)
        self.assertEqual(len1 + 1, len2, "After a new point is added, set length must increase by 1.")
        self.assertIsInstance(space.points, set, "The output points must be a set instance.")
        with self.assertRaises(TypeError):
            space.add_point(22, "1")

    def test_lines(self):
        for p in VALIDATION_POINTS:
            space.add_point(p[0], p[1])
        space.find_collinear_points(3)
        self.assertIsInstance(lns, list, "The output lines must be a list instance.")
        self.assertEqual(len(lns), len(VALIDATION_LINES), "The amount of found solution lines does not equal "
                                                          "to lines in the validation list.")
        for line in lns:
            self.assertIn(set(line), VALIDATION_LINES, "The solution line does not exist in the validation list.")

    def test_clear(self):
        for p in VALIDATION_POINTS:
            space.add_point(p[0], p[1])
        space.clear()
        self.assertEqual(len(pts), 0, "After clearing the space you must have 0 points.")
        self.assertEqual(len(lns), 0, "After clearing the space you must have 0 lines.")

    def test_point_limit(self):
        lim = space.point_limit
        self.assertEqual(lim, 150, "Point limit must equal to 150")


if __name__ == "__main__":
    unittest.main()
