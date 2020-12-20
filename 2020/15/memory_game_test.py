import unittest

from memory_game import memory_game

RESULTS_2020 = [
    ([0, 3, 6], 436),
    ([1, 3, 2], 1),
    ([2, 1, 3], 10),
    ([1, 2, 3], 27),
    ([2, 3, 1], 78),
    ([3, 2, 1], 438),
    ([3, 1, 2], 1836),
]

RESULTS_LARGE = [
    ([0, 3, 6], 175594),
    ([1, 3, 2], 2578),
    ([2, 1, 3], 3544142),
    ([1, 2, 3], 261214),
    ([2, 3, 1], 6895259),
    ([3, 2, 1], 18),
    ([3, 1, 2], 362),
]


class GuessingTests(unittest.TestCase):
    def test_2020(self):
        for nums, result in RESULTS_2020:
            self.assertEqual(memory_game(nums), result)

    def test_large_n(self):
        for nums, result in RESULTS_LARGE:
            self.assertEqual(memory_game(nums, 30000000), result)


if __name__ == "__main__":
    unittest.main()
