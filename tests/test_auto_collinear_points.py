import unittest
from main import lines_from_points, collinear_points


class TestSolution(unittest.TestCase):

    def test_amount_of_lines(self):
        self.assertEqual(len(solution), len(VALIDATION_LINES),
                         "The amount of found solution lines does not equal to lines in the validation list.")

    def test_solution_lines(self):
        for line in solution:
            self.assertIn(line, VALIDATION_LINES,
                          "The solution line does not exist in the validation list.")


VALIDATION_LINES = [{(-9, -7), (-7, -6), (-5, -5), (1, -2)},
                    {(-6, 6), (0, 0), (9, -9)},
                    {(-7, -6), (3, 4), (6, 7)},
                    {(2, -5), (4, 1), (6, 7)}]

INPUT_POINTS = {(-9, -1), (-9, -7), (-8, 3), (-7, -6), (-6, 6), (-5, -5), (-4, -8), (-3, 7), (0, 0),
                 (1, -2), (2, -5), (3, 4), (4, 1), (4, 0), (6, 7), (6, -7), (7, 9), (8, -6), (9, -9)}
input_lines = lines_from_points(INPUT_POINTS)

solution = collinear_points(INPUT_POINTS, input_lines)


if __name__ == "__main__":
    unittest.main()
