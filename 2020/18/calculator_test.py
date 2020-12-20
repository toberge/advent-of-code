import unittest

from calculator import evaluate_advanced, evaluate_simple

PART_ONE_RESULTS = [
    71,
    51,
    26,
    437,
    12240,
    13632,
]

PART_TWO_RESULTS = [
    231,
    51,
    46,
    1445,
    669060,
    23340,
]

EXPRESSIONS = [
    "1 + 2 * 3 + 4 * 5 + 6",
    "1 + (2 * 3) + (4 * (5 + 6))",
    "2 * 3 + (4 * 5)",
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
]


class CalculatorTest(unittest.TestCase):
    def test_part_one(self):
        for expression, output in zip(EXPRESSIONS, PART_ONE_RESULTS):
            self.assertEqual(evaluate_simple(expression), output)

    def test_part_two(self):
        for expression, output in zip(EXPRESSIONS, PART_TWO_RESULTS):
            self.assertEqual(evaluate_advanced(expression), output)


if __name__ == "__main__":
    unittest.main()
