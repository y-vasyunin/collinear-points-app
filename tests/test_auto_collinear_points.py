import unittest
from main import lines_from_points, collinear_points
from validation_data import VALIDATION_POINTS, VALIDATION_LINES


class TestSolution(unittest.TestCase):

    def test_amount_of_lines(self):
        self.assertEqual(len(solution), len(VALIDATION_LINES),
                         "The amount of found solution lines does not equal to lines in the validation list.")

    def test_solution_lines(self):
        for line in solution:
            self.assertIn(line, VALIDATION_LINES,
                          "The solution line does not exist in the validation list.")



all_lines = lines_from_points(VALIDATION_POINTS)

solution = collinear_points(VALIDATION_POINTS, all_lines)


if __name__ == "__main__":
    unittest.main()
